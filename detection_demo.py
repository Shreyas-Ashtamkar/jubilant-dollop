from yolov3.utils import Load_Yolo_model, detect_realtime
from yolov3.configs import YOLO_INPUT_SIZE

video_path   = "http://378e8c3233a6.ngrok.io"

yolo = Load_Yolo_model()

# detect_video_realtime_mp(
#     video_path        = video_path      , 
#     output_path       = ''              , 
#     input_size        = YOLO_INPUT_SIZE , 
#     show              = True            , 
#     rectangle_colors  = (255,0,0)       , 
#     realtime          = True
# )

detect_realtime(
    video_path          = video_path   ,
    Yolo                = yolo         ,
    output_path         = ''           , 
    show                = True         ,
    score_threshold     = 0.4          ,
    rectangle_colors    = (255,0,0)
)
