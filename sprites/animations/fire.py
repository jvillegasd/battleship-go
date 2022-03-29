import os
from sprites.animations.asset import AssetAnimation


class Fire(AssetAnimation):

    def __init__(self, pos_x, pos_y) -> None:
        animation_path = os.path.join('assets', 'fire')
        super().__init__(animation_path, pos_x, pos_y)
