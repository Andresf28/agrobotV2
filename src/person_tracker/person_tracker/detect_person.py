import rclpy
from rclpy.node import Node
from sensor_msgs.msg        import Image
from geometry_msgs.msg      import Point
from cv_bridge              import CvBridge, CvBridgeError
import cv2
from ultralytics import YOLO
import numpy as np

class DetectPerson(Node):

    def __init__(self):
        super().__init__('detect_person')

        self.get_logger().info('Looking person...')
        self.image_sub = self.create_subscription(Image,"/camera/image_raw/uncompressed",self.callback,10)
        self.image_out_pub = self.create_publisher(Image, "/image_out", 1)
        self.ball_pub  = self.create_publisher(Point,"/detected_person",1)

        # self.declare_parameter('tuning_mode', False)

        # self.declare_parameter("x_min",0)
        # self.declare_parameter("x_max",100)
        # self.declare_parameter("y_min",0)
        # self.declare_parameter("y_max",100)
        # self.declare_parameter("h_min",0)
        # self.declare_parameter("h_max",180)
        # self.declare_parameter("s_min",0)
        # self.declare_parameter("s_max",255)
        # self.declare_parameter("v_min",0)
        # self.declare_parameter("v_max",255)
        # self.declare_parameter("sz_min",0)
        # self.declare_parameter("sz_max",100)
        
        # self.tuning_mode = self.get_parameter('tuning_mode').get_parameter_value().bool_value
        # self.tuning_params = {
        #     'x_min': self.get_parameter('x_min').get_parameter_value().integer_value,
        #     'x_max': self.get_parameter('x_max').get_parameter_value().integer_value,
        #     'y_min': self.get_parameter('y_min').get_parameter_value().integer_value,
        #     'y_max': self.get_parameter('y_max').get_parameter_value().integer_value,
        #     'h_min': self.get_parameter('h_min').get_parameter_value().integer_value,
        #     'h_max': self.get_parameter('h_max').get_parameter_value().integer_value,
        #     's_min': self.get_parameter('s_min').get_parameter_value().integer_value,
        #     's_max': self.get_parameter('s_max').get_parameter_value().integer_value,
        #     'v_min': self.get_parameter('v_min').get_parameter_value().integer_value,
        #     'v_max': self.get_parameter('v_max').get_parameter_value().integer_value,
        #     'sz_min': self.get_parameter('sz_min').get_parameter_value().integer_value,
        #     'sz_max': self.get_parameter('sz_max').get_parameter_value().integer_value
        # }
        print("hola1")
        self.bridge = CvBridge()
        self.model = YOLO("yolov8n-seg.pt")
        print("hola 2")
        # if(self.tuning_mode):
        #     proc.create_tuning_window(self.tuning_params)

    def callback(self,data):
        
        cv_image = self.bridge.imgmsg_to_cv2(data)
           
            

        # YOLOOO
        results = self.model.predict(source=cv_image, stream=True, show=False, classes=[0], verbose = False)
        for r in results:       
    
            boxes=r.boxes
            masks = r.masks
            probs = r.probs

            np_boxes=boxes.data.cpu().numpy()
            

            mascara = np.zeros((480,640))
            # HAY QUE VER LA MANERA DE QUE COJA TODOS LOS BBXES Y QUE HAGA LOS RECTANGULOS --- no
            try:
                x_centro = int((np_boxes[0][0] + np_boxes[0][2])/2)
                y_centro = int((np_boxes[0][1] + np_boxes[0][3])/2)

                largo = int(y_centro - np_boxes[0][1])
                ancho = int(x_centro - np_boxes[0][0] )
        
                #cv2.rectangle(mascara,(int(np_boxes[0][0]),int(np_boxes[0][1])),(int(np_boxes[0][2]),int(np_boxes[0][3])), (255,255,255), 3)
                resultante = cv2.ellipse(mascara,(x_centro,y_centro),(largo,ancho),90,0,360,(255,255,255),-1)
                #cv2.imshow("negro",resultante)
                keypoints_norm, out_image = self.blob_detector(resultante)
                cv2.imshow("out",out_image)

                img_to_pub = self.bridge.cv2_to_imgmsg(out_image)
                img_to_pub.header = data.header
                self.image_out_pub.publish(img_to_pub)

                point_out = Point()
    
                # Keep the biggest point
                # They are already converted to normalised coordinates
                for i, kp in enumerate(keypoints_norm):
                    x = kp.pt[0]
                    y = kp.pt[1]
                    s = kp.size
                    self.get_logger().info(f"Pt {i}: ({x},{y},{s})")

                    if (s > point_out.z):                    
                        point_out.x = x
                        point_out.y = y
                        point_out.z = s

                if (point_out.z > 0):
                    self.ball_pub.publish(point_out) 
    


            except:
                cv2.imshow("negro",mascara)
                print("hola")
        


# ------------------------------------------------------------------------------------------------------------

    def blob_detector(self,image):
                  
        image = 255-image
        params = cv2.SimpleBlobDetector_Params()

        params.filterByArea = False
        # params.minArea = 10
        # params.maxArea = 20000

        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = True
        params.minInertiaRatio = 0.01
    
        # # Change thresholds
        # params.minThreshold = 0
        # params.maxThreshold = 100
            
        # # Filter by Area.
        # params.filterByArea = True
        # params.minArea = 30
        # params.maxArea = 20000
            
        # # Filter by Circularity
        # params.filterByCircularity = True
        # params.minCircularity = 0.1
            
        # # Filter by Convexity
        # params.filterByConvexity = True
        # params.minConvexity = 0.5
            
        # # Filter by Inertia
        # params.filterByInertia =True
        # params.minInertiaRatio = 0.5

        detector = cv2.SimpleBlobDetector_create(params)
        # Run detection!
        image = cv2.convertScaleAbs(image)
        keypoints = detector.detect(image)

        size_min_px = 0*image.shape[1]/100.0
        size_max_px = 100*image.shape[1]/100.0

        keypoints = [k for k in keypoints if k.size > size_min_px and k.size < size_max_px]
        
        # Set up main output image
        line_color=(0,0,255)

        out_image = cv2.drawKeypoints(image, keypoints, np.array([]), line_color, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #out_image = draw_window2(out_image, search_window_px)

        # Set up tuning output image
        


        keypoints_normalised = [self.normalise_keypoint(image, k) for k in keypoints]

        return keypoints_normalised, out_image
    
    def normalise_keypoint(self,cv_image, kp):
        rows = float(cv_image.shape[0])
        cols = float(cv_image.shape[1])
        # print(rows, cols)
        center_x    = 0.5*cols
        center_y    = 0.5*rows
        # print(center_x)
        x = (kp.pt[0] - center_x)/(center_x)
        y = (kp.pt[1] - center_y)/(center_y)
        return cv2.KeyPoint(x, y, kp.size/cv_image.shape[1])

# ---------------------------------------------------------------------------------------------------------------------------------------

              


def main(args=None):

    rclpy.init(args=args)

    detect_person = DetectPerson()
    while rclpy.ok():
        rclpy.spin(detect_person)
        

    detect_person.destroy_node()
    rclpy.shutdown()