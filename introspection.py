"""
Introspection system for Chain game.

Allows Cmd+clicking on any game element to open Cursor at the source code
that renders that element.

Usage:
    from introspection import introspect

    # Wrap any draw call to track it:
    introspect.draw(surface, image, rect, "element_name")
    
    # Or use the decorator on draw methods:
    @introspect.track
    def draw(self, surface, camera_offset):
        ...
    
    # In the game loop:
    introspect.begin_frame()  # Clear previous frame's data
    # ... all draw calls ...
    introspect.handle_click(event)  # Check for Cmd+click
"""

import inspect
import os
import sys
import webbrowser
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any
import pygame


@dataclass
class SourceLocation:
    """Represents a location in source code."""
    filepath: str
    line: int
    function: str
    class_name: Optional[str] = None
    
    def __str__(self):
        if self.class_name:
            return f"{self.filepath}:{self.line} ({self.class_name}.{self.function})"
        return f"{self.filepath}:{self.line} ({self.function})"
    
    def to_cursor_url(self) -> str:
        """Generate a Cursor deeplink URL."""
        # cursor://file/<absolute_path>:<line>
        abs_path = os.path.abspath(self.filepath)
        return f"cursor://file/{abs_path}:{self.line}"


@dataclass  
class DrawnElement:
    """Represents an element that was drawn to the screen."""
    name: str
    rect: pygame.Rect
    source_stack: List[SourceLocation]
    z_index: int = 0  # Higher = drawn later (on top)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if a point is within this element's bounds."""
        return self.rect.collidepoint(x, y)


class IntrospectionSystem:
    """
    Tracks all rendered elements and enables Cmd+click inspection.
    """
    
    def __init__(self):
        self.elements: List[DrawnElement] = []
        self.z_counter = 0
        self.enabled = True
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
        # Visual feedback
        self.show_overlay = False
        self.hovered_elements: List[DrawnElement] = []
        self.last_click_elements: List[DrawnElement] = []
        
        # Fonts for overlay (lazy init)
        self._overlay_font = None
        self._overlay_font_small = None
    
    @property
    def overlay_font(self):
        if self._overlay_font is None:
            pygame.font.init()
            self._overlay_font = pygame.font.Font(None, 24)
        return self._overlay_font
    
    @property
    def overlay_font_small(self):
        if self._overlay_font_small is None:
            pygame.font.init()
            self._overlay_font_small = pygame.font.Font(None, 18)
        return self._overlay_font_small
    
    def begin_frame(self):
        """Clear tracking data for a new frame."""
        self.elements.clear()
        self.z_counter = 0
    
    def _get_source_stack(self, skip_frames: int = 2) -> List[SourceLocation]:
        """
        Get the call stack with source locations.
        
        Args:
            skip_frames: Number of frames to skip (internal calls)
        """
        stack = []
        
        for frame_info in inspect.stack()[skip_frames:]:
            filepath = frame_info.filename
            
            # Only include frames from our project
            if not self._is_project_file(filepath):
                continue
            
            # Get relative path for cleaner display
            try:
                rel_path = os.path.relpath(filepath, self.project_root)
            except ValueError:
                rel_path = filepath
            
            # Try to get class name if in a method
            class_name = None
            if 'self' in frame_info.frame.f_locals:
                class_name = type(frame_info.frame.f_locals['self']).__name__
            elif 'cls' in frame_info.frame.f_locals:
                class_name = frame_info.frame.f_locals['cls'].__name__
            
            stack.append(SourceLocation(
                filepath=rel_path,
                line=frame_info.lineno,
                function=frame_info.function,
                class_name=class_name
            ))
        
        return stack
    
    def _is_project_file(self, filepath: str) -> bool:
        """Check if a file is part of our project."""
        try:
            abs_path = os.path.abspath(filepath)
            return abs_path.startswith(self.project_root)
        except (ValueError, OSError):
            return False
    
    def draw(self, 
             surface: pygame.Surface, 
             image: pygame.Surface, 
             pos: Tuple[int, int],
             name: str = "unknown",
             metadata: Dict[str, Any] = None,
             skip_frames: int = 2) -> None:
        """
        Draw an image and track it for introspection.
        
        Args:
            surface: The surface to draw on
            image: The image/surface to draw
            pos: (x, y) position to draw at
            name: Human-readable name for this element
            metadata: Additional data to associate with this element
            skip_frames: Stack frames to skip when getting source
        """
        # Perform the actual draw
        surface.blit(image, pos)
        
        if not self.enabled:
            return
        
        # Track the element
        rect = pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())
        source_stack = self._get_source_stack(skip_frames + 1)
        
        self.elements.append(DrawnElement(
            name=name,
            rect=rect,
            source_stack=source_stack,
            z_index=self.z_counter,
            metadata=metadata or {}
        ))
        self.z_counter += 1
    
    def draw_rect(self,
                  surface: pygame.Surface,
                  color: Tuple[int, ...],
                  rect: pygame.Rect,
                  width: int = 0,
                  name: str = "rect",
                  metadata: Dict[str, Any] = None,
                  skip_frames: int = 2) -> None:
        """
        Draw a rectangle and track it for introspection.
        """
        pygame.draw.rect(surface, color, rect, width)
        
        if not self.enabled:
            return
        
        source_stack = self._get_source_stack(skip_frames + 1)
        
        self.elements.append(DrawnElement(
            name=name,
            rect=pygame.Rect(rect),  # Copy the rect
            source_stack=source_stack,
            z_index=self.z_counter,
            metadata=metadata or {}
        ))
        self.z_counter += 1
    
    def track_region(self,
                     rect: pygame.Rect,
                     name: str,
                     metadata: Dict[str, Any] = None,
                     skip_frames: int = 2) -> None:
        """
        Track a screen region without drawing anything.
        Useful for tracking logical areas like "HUD region" or "game area".
        """
        if not self.enabled:
            return
        
        source_stack = self._get_source_stack(skip_frames + 1)
        
        self.elements.append(DrawnElement(
            name=name,
            rect=pygame.Rect(rect),
            source_stack=source_stack,
            z_index=self.z_counter,
            metadata=metadata or {}
        ))
        self.z_counter += 1
    
    def get_elements_at(self, x: int, y: int) -> List[DrawnElement]:
        """
        Get all elements at a screen position, sorted by z-index (top first).
        """
        elements = [e for e in self.elements if e.contains_point(x, y)]
        return sorted(elements, key=lambda e: e.z_index, reverse=True)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events for introspection.
        
        Returns True if the event was consumed (Cmd+click happened).
        """
        if not self.enabled:
            return False
        
        # Toggle overlay with Cmd+Shift+I
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_i and (mods & pygame.KMOD_META) and (mods & pygame.KMOD_SHIFT):
                self.show_overlay = not self.show_overlay
                return True
        
        # Handle Cmd+click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_META:  # Cmd key on macOS
                x, y = event.pos
                elements = self.get_elements_at(x, y)
                
                if elements:
                    self.last_click_elements = elements
                    self._open_in_cursor(elements)
                    return True
        
        # Track mouse position for hover overlay
        if event.type == pygame.MOUSEMOTION and self.show_overlay:
            x, y = event.pos
            self.hovered_elements = self.get_elements_at(x, y)
        
        return False
    
    def _open_in_cursor(self, elements: List[DrawnElement]) -> None:
        """
        Open Cursor at the source location of elements.
        Opens all unique source locations from the top element's stack.
        """
        if not elements:
            return
        
        # Get the topmost element (most recently drawn)
        top_element = elements[0]
        
        print(f"\n{'='*60}")
        print(f"🔍 INTROSPECTION: Clicked on '{top_element.name}'")
        print(f"{'='*60}")
        
        # Print the full element stack at this position
        print(f"\n📚 Element stack at this position ({len(elements)} elements):")
        for i, elem in enumerate(elements):
            z_info = f"z={elem.z_index}"
            print(f"  {i+1}. {elem.name} [{z_info}]")
            if elem.metadata:
                print(f"      metadata: {elem.metadata}")
        
        # Print and open the source stack for the top element
        print(f"\n📍 Source stack for '{top_element.name}':")
        opened_first = False
        
        for i, loc in enumerate(top_element.source_stack):
            prefix = "  → " if i == 0 else "    "
            print(f"{prefix}{loc}")
            
            # Open the first (most specific) location in Cursor
            if not opened_first:
                url = loc.to_cursor_url()
                print(f"\n🚀 Opening in Cursor: {url}")
                try:
                    webbrowser.open(url)
                    opened_first = True
                except Exception as e:
                    print(f"   ⚠️  Failed to open: {e}")
        
        print(f"{'='*60}\n")
    
    def draw_overlay(self, surface: pygame.Surface) -> None:
        """
        Draw the debug overlay showing element boundaries and info.
        """
        if not self.show_overlay:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw all element boundaries (faintly)
        for elem in self.elements:
            color = (100, 100, 100, 50)
            pygame.draw.rect(surface, color[:3], elem.rect, 1)
        
        # Highlight hovered elements
        for i, elem in enumerate(self.hovered_elements):
            # Color based on z-order
            hue = (elem.z_index * 30) % 360
            # Simple HSV to RGB approximation
            if hue < 60:
                color = (255, int(hue * 4.25), 0)
            elif hue < 120:
                color = (int((120 - hue) * 4.25), 255, 0)
            elif hue < 180:
                color = (0, 255, int((hue - 120) * 4.25))
            elif hue < 240:
                color = (0, int((240 - hue) * 4.25), 255)
            elif hue < 300:
                color = (int((hue - 240) * 4.25), 0, 255)
            else:
                color = (255, 0, int((360 - hue) * 4.25))
            
            # Draw highlighted border
            pygame.draw.rect(surface, color, elem.rect, 2)
        
        # Draw info panel for hovered elements
        if self.hovered_elements:
            self._draw_info_panel(surface, mouse_pos)
    
    def _draw_info_panel(self, surface: pygame.Surface, mouse_pos: Tuple[int, int]) -> None:
        """Draw info panel showing hovered element details."""
        if not self.hovered_elements:
            return
        
        # Build info text
        lines = [
            f"Elements at cursor: {len(self.hovered_elements)}",
            "─" * 30,
        ]
        
        for elem in self.hovered_elements[:5]:  # Show top 5
            lines.append(f"• {elem.name} (z={elem.z_index})")
            if elem.source_stack:
                loc = elem.source_stack[0]
                lines.append(f"  {loc.filepath}:{loc.line}")
        
        if len(self.hovered_elements) > 5:
            lines.append(f"  ... and {len(self.hovered_elements) - 5} more")
        
        lines.append("─" * 30)
        lines.append("Cmd+Click to open in Cursor")
        lines.append("Cmd+Shift+I to toggle overlay")
        
        # Calculate panel size
        padding = 10
        line_height = 18
        max_width = max(self.overlay_font_small.size(line)[0] for line in lines)
        panel_width = max_width + padding * 2
        panel_height = len(lines) * line_height + padding * 2
        
        # Position panel near mouse but keep on screen
        panel_x = mouse_pos[0] + 15
        panel_y = mouse_pos[1] + 15
        
        if panel_x + panel_width > surface.get_width():
            panel_x = mouse_pos[0] - panel_width - 15
        if panel_y + panel_height > surface.get_height():
            panel_y = mouse_pos[1] - panel_height - 15
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Semi-transparent background
        overlay_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        overlay_surface.fill((20, 20, 30, 230))
        surface.blit(overlay_surface, (panel_x, panel_y))
        
        # Border
        pygame.draw.rect(surface, (100, 200, 255), panel_rect, 2)
        
        # Draw text
        y = panel_y + padding
        for line in lines:
            if line.startswith("─"):
                color = (80, 80, 100)
            elif line.startswith("•"):
                color = (255, 255, 100)
            elif line.startswith("  "):
                color = (150, 200, 255)
            elif "Cmd" in line:
                color = (100, 255, 150)
            else:
                color = (255, 255, 255)
            
            text = self.overlay_font_small.render(line, True, color)
            surface.blit(text, (panel_x + padding, y))
            y += line_height


# Global instance
introspect = IntrospectionSystem()


# Decorator for tracking draw methods
def tracked(name: str = None):
    """
    Decorator to track a draw method for introspection.
    
    Usage:
        @tracked("player")
        def draw(self, surface, camera_offset):
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get 'self' if this is a method
            element_name = name
            if not element_name and args:
                element_name = type(args[0]).__name__
            
            # Call the original function
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


# Convenience function for simple draw tracking
def draw_tracked(surface: pygame.Surface, 
                 image: pygame.Surface, 
                 pos: Tuple[int, int],
                 name: str = "sprite") -> None:
    """
    Draw an image with introspection tracking.
    
    This is a convenience function that wraps surface.blit() with tracking.
    """
    introspect.draw(surface, image, pos, name, skip_frames=3)
