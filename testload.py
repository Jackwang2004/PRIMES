


import numpy as np
import cv2,os,json


def load_imgs(args):


    print("Dataset path: %s"%(args.dataset))
    images = os.path.join(args.dataset, "/images")
    path_images = os.listdir(images)


    img =  cv2.imread(os.path.join(images, path_images[0]))
    h_res,w_res,_ = img.shape
    h_res = h_res//args.factor
    w_res = w_res//args.factor
    num_n = args.num_n

    print('Downsampling factor: %d'%(args.factor))
    print('Output resolution: %d x %d'%(h_res,w_res))
    dims = args.dim

    path = os.path.join(args.dataset, "/details.log")
    details = open(path)

    coordinates = []
    training_pairs = []
    images      = []

    controls = args.type

    for line in details:

        #coordinates
        coorddict = line.get("render_args")
        coordinate = []
        for control in controls:
            coordinate.append(coorddict.get(control))
        coordinates.append(np.array(coordinate))

        #images
        id = line.get("id")
        img =  cv2.imread(os.path.join(images, id)
        img = cv2.resize(img,None,fx=1/args.factor,fy=1/args.factor, interpolation = cv2.INTER_AREA)
        img = np.float32(img)/255.0
        images.append(img)

    #training pairs
    for coordinate in coordinates:
        for i in range(0, len(controls)):
            pair = []
            sameother = []

            pair.append(coordinate)
            for other in coordinates:
                same = True
                for j in range(0, i):
                    if coordinate[j]!=other[j]:
                        same = False
                for k in range(i+1,len(coordinates)):
                    if coordinate[k]!=other[k]:
                        same = False
                if(same):
                    sameother.append(other)
            for option in sameother:
                closesthigh = None
                closestlow = None
                higher = option[i] > coordinate[i]:
                if(higher):
                    if closesthigh == None:
                        closesthigh = option
                    elif option[i]<closesthigh[i]:
                        closesthigh = option
                else:
                    if closestlow == None:
                        closestlow = option
                    elif option[i]>closestlow[i]:
                        closestlow = option
                if closesthigh == None:
                    secondclosestlow = None
                    for option in sameother:
                        lower = option[i] < closestlow[i]
                        if lower:
                            if secondclosestlow = None:
                                secondclosestlow = option
                            elif option[i]>secondclosestlow[i]:
                                secondclosestlow = option
                    closesthigh = secondclosestlow

                if closestlow == None:
                    secondclosesthigh = None
                    for option in sameother:
                        higher = option[i] > closesthigh[i]
                        if higher:
                            if secondclosesthigh = None:
                                secondclosesthigh = option
                            elif option[i]<secondclosesthigh[i]:
                                secondclosesthigh = option
                    closestlow = secondclosesthigh

                albedo = []
                pair.append(closestlow)
                pair.append(closesthigh)



    return images,coordinates,training_pairs,h_res,w_res
