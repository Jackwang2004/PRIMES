import argparse
import numpy as np
import cv2,os,json


def load_imgs(args):

    print("Dataset path: %s"%(args.dataset))
    path_images = os.path.join(args.dataset, "images")
    images = os.listdir(path_images)

    img =  cv2.imread(os.path.join(path_images, images[0]))
    h_res,w_res,_ = img.shape
    h_res = h_res//args.factor
    w_res = w_res//args.factor
    num_n = args.num_n

    print('Downsampling factor: %d'%(args.factor))
    print('Output resolution: %d x %d'%(h_res,w_res))
    dims = args.dim

    path = os.path.join(args.dataset, "details.log")
    details = open(path)

    coordinates = []
    training_pairs = []
    storeimages      = []

    controls = args.type

    for object in details:
        line = json.loads(object)

        #coordinates
        coorddict = line.get("render_args")
        coordinate = []
        for control in controls:
            coordinate.append(coorddict.get(control))
        coordinates.append(np.array(coordinate))

        #images
        id = line.get("id")
        img =  cv2.imread(os.path.join(path_images, id+"_rgb.png"))
        img = cv2.resize(img,None,fx=1/args.factor,fy=1/args.factor, interpolation = cv2.INTER_AREA)
        img = np.float32(img)/255.0
        storeimages.append(img)

        #DEBUGGED, WORKS

    #training pairs
    for coordinate in coordinates:
        for i in range(0, len(controls)):
            pair = []
            sameother = []
            pair.append(coordinate)
            for other in coordinates:
                same = True
                for j in range(0, len(other)):
                    if coordinate[j]!=other[j] and not np.array_equal(coordinate, other):
                        same = False
                if(same):
                    sameother.append(other)

            closesthigh = None
            closestlow = None

            #DEBUGGED, WORKS

            for option in sameother:
                higher = option[i] > coordinate[i]
                if higher:
                    if closesthigh is None:
                        closesthigh = option
                    else:
                        closesthigh = option
                else:
                    if closestlow is None:
                        closestlow = option
                    else:
                        closestlow = option

                if closesthigh is None:
                    secondclosestlow = None
                    for option in sameother:
                        lower = option[i] < closestlow[i]
                        if lower:
                            if secondclosestlow is None:
                                secondclosestlow = option
                            elif option[i]>secondclosestlow[i]:
                                secondclosestlow = option
                    closesthigh = secondclosestlow

                if closestlow is None:
                    secondclosesthigh = None
                    for option in sameother:
                        higher = option[i] > closesthigh[i]
                        if higher:
                            if secondclosesthigh is None:
                                secondclosesthigh = option
                            elif option[i]<secondclosesthigh[i]:
                                secondclosesthigh = option
                    closestlow = secondclosesthigh

            pair.append(closestlow)
            pair.append(closesthigh)

            light = None
            for k in range(len(controls)):
                if controls[k]=="light":
                    light = k
            albedo = coordinate
            if(light is not None):
                albedo[light] = 0
            pair.append(albedo)
            training_pairs.append(pair)

    print(np.array(storeimages).shape)
    print(np.array(coordinates).shape)
    print(np.array(training_pairs).shape)
    print(h_res)
    print(w_res)
    return storeimages,coordinates,training_pairs,h_res,w_res
