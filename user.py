from dataclasses import dataclass


@dataclass
class User:
    chat_id: int
    crop: tuple
    good_frames: int
    bad_frames: int
    user_frames: list
