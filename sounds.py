"""
Sound and music system for Chain
Uses procedurally generated sounds and music
"""

import pygame
import math
import array


def init_sound():
    """Initialize the sound system"""
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)


def generate_square_wave(frequency, duration, volume=0.3):
    """Generate a square wave sound"""
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    
    buf = array.array('h')
    amplitude = int(32767 * volume)
    
    period = sample_rate / frequency
    
    for i in range(n_samples):
        if (i / period) % 1 < 0.5:
            buf.append(amplitude)
        else:
            buf.append(-amplitude)
    
    # Stereo
    stereo_buf = array.array('h')
    for sample in buf:
        stereo_buf.append(sample)
        stereo_buf.append(sample)
    
    sound = pygame.mixer.Sound(buffer=stereo_buf)
    return sound


def generate_noise(duration, volume=0.2):
    """Generate white noise"""
    import random
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    
    buf = array.array('h')
    amplitude = int(32767 * volume)
    
    for i in range(n_samples):
        buf.append(random.randint(-amplitude, amplitude))
    
    # Stereo
    stereo_buf = array.array('h')
    for sample in buf:
        stereo_buf.append(sample)
        stereo_buf.append(sample)
    
    sound = pygame.mixer.Sound(buffer=stereo_buf)
    return sound


def generate_melody(notes, tempo=120, volume=0.25):
    """Generate a melody from a list of (note, duration) tuples"""
    sample_rate = 22050
    beat_duration = 60 / tempo
    
    all_samples = array.array('h')
    
    # Note frequencies (A4 = 440Hz)
    note_freqs = {
        'C2': 65.41, 'D2': 73.42, 'E2': 82.41, 'F2': 87.31,
        'G2': 98.00, 'A2': 110.00, 'B2': 123.47,
        'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 
        'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
        'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
        'REST': 0
    }
    
    for note, beats in notes:
        duration = beat_duration * beats
        n_samples = int(sample_rate * duration)
        
        if note == 'REST' or note not in note_freqs:
            # Silence
            for _ in range(n_samples):
                all_samples.append(0)
        else:
            freq = note_freqs[note]
            amplitude = int(32767 * volume)
            period = sample_rate / freq if freq > 0 else 1
            
            for i in range(n_samples):
                # Square wave with envelope
                envelope = 1.0
                if i < n_samples * 0.1:
                    envelope = i / (n_samples * 0.1)
                elif i > n_samples * 0.7:
                    envelope = (n_samples - i) / (n_samples * 0.3)
                
                if (i / period) % 1 < 0.5:
                    all_samples.append(int(amplitude * envelope))
                else:
                    all_samples.append(int(-amplitude * envelope))
    
    # Stereo
    stereo_buf = array.array('h')
    for sample in all_samples:
        stereo_buf.append(sample)
        stereo_buf.append(sample)
    
    sound = pygame.mixer.Sound(buffer=stereo_buf)
    return sound


def generate_chiptune_track(melody, bass, tempo=120, volume=0.2):
    """Generate a full chiptune track with melody, bass, and drums"""
    import random
    sample_rate = 22050
    beat_duration = 60 / tempo
    
    # Note frequencies
    note_freqs = {
        'C2': 65.41, 'D2': 73.42, 'E2': 82.41, 'F2': 87.31,
        'G2': 98.00, 'A2': 110.00, 'B2': 123.47,
        'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 
        'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
        'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
        'REST': 0
    }
    
    # Calculate total duration
    total_beats = sum(beats for _, beats in melody)
    total_samples = int(sample_rate * beat_duration * total_beats)
    
    # Generate each channel
    melody_samples = array.array('h', [0] * total_samples)
    bass_samples = array.array('h', [0] * total_samples)
    drum_samples = array.array('h', [0] * total_samples)
    arp_samples = array.array('h', [0] * total_samples)
    
    # Generate melody (square wave, 25% duty cycle for that classic sound)
    sample_pos = 0
    for note, beats in melody:
        duration = beat_duration * beats
        n_samples = int(sample_rate * duration)
        
        if note != 'REST' and note in note_freqs:
            freq = note_freqs[note]
            amplitude = int(32767 * volume * 0.5)
            period = sample_rate / freq if freq > 0 else 1
            
            for i in range(min(n_samples, total_samples - sample_pos)):
                # 25% duty cycle square wave
                envelope = 1.0
                if i < n_samples * 0.05:
                    envelope = i / (n_samples * 0.05)
                elif i > n_samples * 0.8:
                    envelope = (n_samples - i) / (n_samples * 0.2)
                
                duty = 0.25
                if (i / period) % 1 < duty:
                    melody_samples[sample_pos + i] = int(amplitude * envelope)
                else:
                    melody_samples[sample_pos + i] = int(-amplitude * envelope * 0.3)
        
        sample_pos += n_samples
    
    # Generate bass (triangle wave for warmer sound)
    sample_pos = 0
    bass_idx = 0
    beats_elapsed = 0
    
    for note, beats in melody:
        duration = beat_duration * beats
        n_samples = int(sample_rate * duration)
        
        # Get corresponding bass note
        if bass_idx < len(bass):
            bass_note, bass_beats = bass[bass_idx % len(bass)]
            if bass_note != 'REST' and bass_note in note_freqs:
                freq = note_freqs[bass_note]
                amplitude = int(32767 * volume * 0.4)
                period = sample_rate / freq if freq > 0 else 1
                
                for i in range(min(n_samples, total_samples - sample_pos)):
                    # Triangle wave
                    t = (i / period) % 1
                    if t < 0.5:
                        val = t * 4 - 1
                    else:
                        val = 3 - t * 4
                    bass_samples[sample_pos + i] = int(amplitude * val * 0.7)
        
        sample_pos += n_samples
        beats_elapsed += beats
        if beats_elapsed >= (bass[bass_idx % len(bass)][1] if bass_idx < len(bass) else 1):
            bass_idx += 1
            beats_elapsed = 0
    
    # Generate drums (noise kicks and hi-hats)
    beat_samples = int(sample_rate * beat_duration)
    for beat in range(int(total_beats)):
        start = beat * beat_samples
        
        # Kick on beats 1 and 3 (every 2 beats in 4/4)
        if beat % 2 == 0:
            kick_len = min(int(beat_samples * 0.15), total_samples - start)
            for i in range(kick_len):
                # Descending pitch noise burst
                freq = 150 - (i / kick_len) * 100
                period = sample_rate / max(freq, 20)
                envelope = 1 - (i / kick_len)
                amplitude = int(32767 * volume * 0.5 * envelope)
                if (i / period) % 1 < 0.5:
                    drum_samples[start + i] += amplitude
                else:
                    drum_samples[start + i] -= amplitude
        
        # Hi-hat on every beat
        hat_start = start + int(beat_samples * 0.5) if beat % 2 == 1 else start
        if hat_start < total_samples:
            hat_len = min(int(beat_samples * 0.08), total_samples - hat_start)
            for i in range(hat_len):
                envelope = 1 - (i / hat_len)
                amplitude = int(32767 * volume * 0.15 * envelope)
                drum_samples[hat_start + i] += random.randint(-amplitude, amplitude)
    
    # Generate arpeggios (fast note sequences for texture)
    arp_notes = ['C4', 'E4', 'G4', 'C5']  # Major chord arpeggio
    arp_speed = beat_duration / 4  # 16th notes
    arp_samples_per_note = int(sample_rate * arp_speed)
    
    for i in range(0, total_samples, arp_samples_per_note):
        note_idx = (i // arp_samples_per_note) % len(arp_notes)
        note = arp_notes[note_idx]
        freq = note_freqs[note]
        amplitude = int(32767 * volume * 0.15)
        period = sample_rate / freq
        
        for j in range(min(arp_samples_per_note, total_samples - i)):
            envelope = 1 - (j / arp_samples_per_note) * 0.7
            # Pulse wave
            if (j / period) % 1 < 0.125:
                arp_samples[i + j] = int(amplitude * envelope)
    
    # Mix all channels
    mixed = array.array('h')
    for i in range(total_samples):
        # Combine and clip
        total = melody_samples[i] + bass_samples[i] + drum_samples[i] + arp_samples[i]
        total = max(-32767, min(32767, total))
        mixed.append(int(total))
    
    # Stereo with slight panning
    stereo_buf = array.array('h')
    for i, sample in enumerate(mixed):
        # Slight stereo variation
        left = int(sample * 0.9)
        right = int(sample * 1.0)
        stereo_buf.append(left)
        stereo_buf.append(right)
    
    return pygame.mixer.Sound(buffer=stereo_buf)


class SoundManager:
    """Manages all game sounds and music"""
    
    def __init__(self):
        init_sound()
        
        self.sounds = {}
        self.music = {}
        self.current_music = None
        self.music_enabled = True
        self.sound_enabled = True
        
        self._generate_sounds()
        self._generate_music()
    
    def _generate_sounds(self):
        """Generate all sound effects"""
        # Attack sound
        self.sounds['attack'] = generate_square_wave(200, 0.1, 0.2)
        
        # Jump sound
        self.sounds['jump'] = self._make_jump_sound()
        
        # Hit sound
        self.sounds['hit'] = generate_noise(0.15, 0.3)
        
        # Pickup sound
        self.sounds['pickup'] = self._make_pickup_sound()
        
        # Spell sounds
        self.sounds['spell'] = generate_square_wave(440, 0.2, 0.2)
        
        # Enemy death
        self.sounds['enemy_death'] = self._make_death_sound()
        
        # Menu select
        self.sounds['menu'] = generate_square_wave(330, 0.1, 0.15)
    
    def _make_jump_sound(self):
        """Create a jump sound effect (rising pitch)"""
        sample_rate = 22050
        duration = 0.15
        n_samples = int(sample_rate * duration)
        
        buf = array.array('h')
        volume = 0.2
        amplitude = int(32767 * volume)
        
        for i in range(n_samples):
            # Rising frequency
            t = i / n_samples
            freq = 150 + t * 400
            period = sample_rate / freq
            
            if (i / period) % 1 < 0.5:
                buf.append(int(amplitude * (1 - t * 0.5)))
            else:
                buf.append(int(-amplitude * (1 - t * 0.5)))
        
        stereo_buf = array.array('h')
        for sample in buf:
            stereo_buf.append(sample)
            stereo_buf.append(sample)
        
        return pygame.mixer.Sound(buffer=stereo_buf)
    
    def _make_pickup_sound(self):
        """Create a pickup sound effect (arpeggio)"""
        sample_rate = 22050
        
        buf = array.array('h')
        volume = 0.2
        amplitude = int(32767 * volume)
        
        freqs = [330, 440, 550, 660]  # Rising arpeggio
        
        for freq in freqs:
            duration = 0.05
            n_samples = int(sample_rate * duration)
            period = sample_rate / freq
            
            for i in range(n_samples):
                envelope = 1 - (i / n_samples) * 0.5
                if (i / period) % 1 < 0.5:
                    buf.append(int(amplitude * envelope))
                else:
                    buf.append(int(-amplitude * envelope))
        
        stereo_buf = array.array('h')
        for sample in buf:
            stereo_buf.append(sample)
            stereo_buf.append(sample)
        
        return pygame.mixer.Sound(buffer=stereo_buf)
    
    def _make_death_sound(self):
        """Create enemy death sound (descending)"""
        sample_rate = 22050
        duration = 0.2
        n_samples = int(sample_rate * duration)
        
        buf = array.array('h')
        volume = 0.25
        amplitude = int(32767 * volume)
        
        for i in range(n_samples):
            t = i / n_samples
            freq = 400 - t * 300
            period = sample_rate / freq if freq > 0 else 1
            
            if (i / period) % 1 < 0.5:
                buf.append(int(amplitude * (1 - t)))
            else:
                buf.append(int(-amplitude * (1 - t)))
        
        stereo_buf = array.array('h')
        for sample in buf:
            stereo_buf.append(sample)
            stereo_buf.append(sample)
        
        return pygame.mixer.Sound(buffer=stereo_buf)
    
    def _generate_music(self):
        """Generate background music tracks with harmony and rhythm"""
        
        # Menu music - calm, mysterious with arpeggios
        menu_melody = [
            ('E4', 1), ('G4', 1), ('A4', 2),
            ('E4', 1), ('G4', 1), ('B4', 2),
            ('A4', 1), ('G4', 1), ('E4', 2),
            ('D4', 1), ('E4', 1), ('G4', 2),
            ('E4', 1), ('G4', 1), ('A4', 2),
            ('G4', 1), ('E4', 1), ('D4', 2),
            ('E4', 4),
            ('REST', 2),
        ]
        menu_bass = [
            ('A2', 4), ('E2', 4),
            ('A2', 4), ('D3', 4),
            ('A2', 4), ('E2', 4),
            ('A2', 2), ('REST', 4),
        ]
        self.music['menu'] = generate_chiptune_track(menu_melody, menu_bass, tempo=85, volume=0.18)
        
        # World map music - adventurous with bouncy rhythm
        world_melody = [
            ('C5', 0.5), ('E5', 0.5), ('G5', 1), ('E5', 0.5), ('C5', 0.5),
            ('D5', 0.5), ('F5', 0.5), ('A5', 1), ('F5', 0.5), ('D5', 0.5),
            ('E5', 0.5), ('G5', 0.5), ('B5', 1), ('G5', 0.5), ('E5', 0.5),
            ('C5', 1), ('G4', 1), ('E4', 1), ('C4', 1),
            ('C5', 0.5), ('D5', 0.5), ('E5', 0.5), ('F5', 0.5), ('G5', 1), ('E5', 1),
            ('A4', 0.5), ('B4', 0.5), ('C5', 0.5), ('D5', 0.5), ('E5', 2),
            ('G4', 1), ('A4', 1), ('B4', 1), ('C5', 1),
            ('E5', 2), ('C5', 2),
        ]
        world_bass = [
            ('C3', 2), ('G2', 2),
            ('D3', 2), ('A2', 2),
            ('E3', 2), ('B2', 2),
            ('C3', 2), ('G2', 2),
            ('C3', 2), ('E3', 2),
            ('A2', 2), ('E3', 2),
            ('G2', 2), ('C3', 2),
            ('C3', 4),
        ]
        self.music['world'] = generate_chiptune_track(world_melody, world_bass, tempo=120, volume=0.18)
        
        # Level music - energetic action with driving beat
        level_melody = [
            ('E5', 0.25), ('E5', 0.25), ('REST', 0.25), ('E5', 0.25),
            ('REST', 0.25), ('C5', 0.25), ('E5', 0.5),
            ('G5', 1), ('G4', 1),
            ('C5', 0.5), ('REST', 0.25), ('G4', 0.25), ('REST', 0.5), ('E4', 0.5),
            ('REST', 0.25), ('A4', 0.5), ('B4', 0.25), ('REST', 0.25), ('A4', 0.25), ('G4', 0.5),
            ('E5', 0.5), ('G5', 0.5), ('A5', 0.5), ('F5', 0.25), ('G5', 0.25),
            ('REST', 0.25), ('E5', 0.5), ('C5', 0.25), ('D5', 0.25), ('B4', 0.5),
            ('C5', 1), ('REST', 1),
        ]
        level_bass = [
            ('C3', 1), ('C3', 1),
            ('G2', 1), ('G2', 1),
            ('C3', 0.5), ('C3', 0.5), ('G2', 0.5), ('G2', 0.5),
            ('A2', 1), ('E2', 1),
            ('C3', 0.5), ('G2', 0.5), ('A2', 0.5), ('F2', 0.5),
            ('G2', 1), ('C3', 1),
        ]
        self.music['level'] = generate_chiptune_track(level_melody, level_bass, tempo=115, volume=0.2)
        
        # Boss music - intense and aggressive
        boss_melody = [
            ('E4', 0.25), ('E4', 0.25), ('E5', 0.25), ('E4', 0.25),
            ('E4', 0.25), ('D5', 0.25), ('E4', 0.25), ('E4', 0.25),
            ('E4', 0.25), ('E4', 0.25), ('E5', 0.25), ('G5', 0.25),
            ('F5', 0.25), ('E5', 0.25), ('D5', 0.5),
            ('A4', 0.25), ('A4', 0.25), ('A5', 0.25), ('A4', 0.25),
            ('A4', 0.25), ('G5', 0.25), ('A4', 0.25), ('A4', 0.25),
            ('B4', 0.25), ('B4', 0.25), ('B5', 0.25), ('A5', 0.25),
            ('G5', 0.25), ('F5', 0.25), ('E5', 0.5),
            ('E5', 0.25), ('REST', 0.25), ('E5', 0.25), ('REST', 0.25),
            ('D5', 0.25), ('REST', 0.25), ('C5', 0.25), ('REST', 0.25),
            ('B4', 0.5), ('A4', 0.5),
            ('G4', 0.25), ('A4', 0.25), ('B4', 0.25), ('C5', 0.25),
            ('D5', 0.25), ('E5', 0.25), ('F5', 0.25), ('G5', 0.25),
            ('A5', 1),
            ('E5', 0.5), ('D5', 0.5),
            ('E5', 1),
        ]
        boss_bass = [
            ('E2', 0.5), ('E2', 0.5), ('E2', 0.5), ('E2', 0.5),
            ('E2', 0.5), ('E2', 0.5), ('E2', 0.5), ('E2', 0.5),
            ('A2', 0.5), ('A2', 0.5), ('A2', 0.5), ('A2', 0.5),
            ('B2', 0.5), ('B2', 0.5), ('B2', 0.5), ('B2', 0.5),
            ('E2', 0.5), ('E2', 0.5), ('D2', 0.5), ('D2', 0.5),
            ('C2', 0.5), ('C2', 0.5), ('B2', 0.5), ('B2', 0.5),
            ('A2', 1), ('E2', 1),
            ('E2', 1), ('E2', 1),
        ]
        self.music['boss'] = generate_chiptune_track(boss_melody, boss_bass, tempo=170, volume=0.22)
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_name):
        """Play background music (loops)"""
        if not self.music_enabled:
            return
        
        if music_name == self.current_music:
            return
        
        # Stop current music
        pygame.mixer.stop()
        
        if music_name in self.music:
            self.current_music = music_name
            # Loop the music by playing it repeatedly
            self.music[music_name].play(loops=-1)
    
    def stop_music(self):
        """Stop all music"""
        pygame.mixer.stop()
        self.current_music = None
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        return self.music_enabled
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled


# Global sound manager instance
_sound_manager = None


def get_sound_manager():
    """Get the global sound manager"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
