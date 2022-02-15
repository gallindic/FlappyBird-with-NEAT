import yaml


def parse_configurations(configuration_file_path):
    with open(configuration_file_path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(-1)


def frames_to_msec(frames, fps):
    """Convert frames to milliseconds at the specified framerate.
    Arguments:
    frames: How many frames to convert to milliseconds.
    fps: The framerate to use for conversion.  Default: FPS.
    """
    return 1000.0 * frames / fps


def msec_to_frames(milliseconds, fps):
    """Convert milliseconds to frames at the specified framerate.
    Arguments:
    milliseconds: How many milliseconds to convert to frames.
    fps: The framerate to use for conversion.  Default: FPS.
    """
    return fps * milliseconds / 1000.0