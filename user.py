from dataclasses import dataclass


@dataclass
class User:
    chat_id: int
    crop: tuple
    good_frames: int
    bad_frames: int
    pose_frames: list

    def set_crop(self, coordinates: tuple):
        self.crop = coordinates

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id
