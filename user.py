from dataclasses import dataclass


@dataclass
class User:
    chat_id: int
    crop: tuple
    good_frames: int
    bad_frames: int
    user_frames: list

    def __init__(self, chat_id, crop):
        self.chat_id = chat_id
        self.crop = crop

