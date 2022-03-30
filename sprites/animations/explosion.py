import os
from sprites.animations.asset import AssetAnimation


class Explosion(AssetAnimation):

    def __init__(
            self,
            pos_x: float,
            pos_y: float,
            stop_after_finish: bool = False) -> None:
        
        animation_path = os.path.join('assets', 'explosion')
        super().__init__(animation_path, pos_x, pos_y, stop_after_finish)
