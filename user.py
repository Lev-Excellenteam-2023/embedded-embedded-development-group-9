from dataclasses import dataclass


@dataclass
class User:
    chat_id: int
    crop: tuple
    good_frames: int
    bad_frames: int
    pose_frames: list

    def __init__(self, chat_id, crop):
        self.chat_id = chat_id
        self.crop = crop
        self.good_frames = 0
        self.bad_frames = 0
        self.user_frames = []

