from dataclasses import dataclass


@dataclass
class User:
    chat_id: int
    crop: tuple
    good_frames: int
    bad_frames: int
    user_frames: list

    def __init__(self, chat_id, crop, good_frames=0, bad_frames=0, user_frames=[]):
        self.chat_id = chat_id
        self.crop = crop
        self.good_frames = good_frames
        self.bad_frames = bad_frames
        self.user_frames = user_frames

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "crop": self.crop,
            "good_frames": self.good_frames,
            "bad_frames": self.bad_frames,
            "user_frames": self.user_frames
        }
