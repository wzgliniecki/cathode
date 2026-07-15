import typer
from cathode.config.settings import RenderSettings, DevSettings
from cathode.app.main import run


def main(
    max_fps: int = RenderSettings.max_fps,
    image_width: int = RenderSettings.image_width,
    image_height: int = RenderSettings.image_height,
    max_frames: int | None = DevSettings.max_frames,
):
    RenderSettings.max_fps = max_fps
    RenderSettings.image_width = image_width
    RenderSettings.image_height = image_height
    DevSettings.max_frames = max_frames

    run()


if __name__ == "__main__":
    typer.run(main)
