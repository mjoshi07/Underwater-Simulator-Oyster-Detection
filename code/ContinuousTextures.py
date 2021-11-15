import cv2
import numpy as np
import random
import os


def smudge_boundaries(img, block_size):
    # WIP: COMPLTETE IT LATER, NOT ON PRIORITY

    # we have to smudge the internal boundaries area which is the center area vertically and horizontally
    h, w = img.shape[:2]

    cv2.namedWindow('final img', cv2.WINDOW_FREERATIO)

    signs = [-1, 1]
    hori_smudge_y = int((h/2.0) - (block_size/2))

    for x in range(0, w, block_size):
        add_sub = random.choice(signs)
        patch_y = int((h / 2.0) + add_sub*2 * block_size)
        img_patch = img[patch_y: patch_y + block_size, x: x + block_size]
        # cv2.imshow('patch img', img_patch)
        # cv2.waitKey(0)
        # print(img_patch.shape)
        img[hori_smudge_y:hori_smudge_y+block_size, x:x + block_size] = img_patch

        img[hori_smudge_y-int(block_size/2):hori_smudge_y+int(block_size/2), x:x+block_size] = \
            cv2.GaussianBlur(img[hori_smudge_y-int(block_size/2):hori_smudge_y+int(block_size/2), x:x+block_size],\
                         (5, 5), 0)

        # print("x: ", x)
        # smudge the center area
        # pass

        cv2.imshow('patch img', img_patch)
        cv2.imshow('final img', img)
        cv2.waitKey(0)

    for y in range(0, h, block_size):
        add_sub = random.choice(signs)
        vert_smudge_x = int((w / 2.0) + add_sub*2 * block_size)
        print("y: ", y)


def stack_img(img1, img2, side="RIGHT"):

    # stack THE imgs according to the side
    if side == "RIGHT":
        stacked_img = np.concatenate((img1, img2), axis=1)
    elif side == "LEFT":
        stacked_img = np.concatenate((img2, img1), axis=1)
    elif side == "BOTTOM":
        stacked_img = np.concatenate((img2, img1), axis=0)
    else:
        # stack img2 on bottom of img1
        stacked_img = np.concatenate((img1, img2), axis=0)

    return stacked_img


def flip_img(img, axis="VERTICAL"):

    # do flipping about the axis
    if axis == "HORIZONTAL":
        flipped_img = cv2.flip(img, 0)
    elif axis == "VERTICAL":
        flipped_img = cv2.flip(img, 1)
    else:
        flipped_img = img

    return flipped_img


def continuous_texture(img_dir, block_size=10, display_tex=True, save_tex=False, out_dir=None):
    
    if display_tex:
        cv2.namedWindow('original tex', cv2.WINDOW_FREERATIO)
        cv2.namedWindow('continuous tex', cv2.WINDOW_FREERATIO)

    if save_tex:
        if out_dir is None:
            # create a dir next to textures dir named continuous_textures and save textures in it
            base_dir = img_dir.split("textures")[0]
            out_dir = os.path.join(base_dir, "continuous_textures")
            
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

    for root, dir, files in os.walk(img_dir):
        for img_filename in files:
            img_path = os.path.join(root, img_filename)

            og_tex = cv2.imread(img_path)

            # flip about the Right side
            horizontal_flip = flip_img(og_tex, "VERTICAL")

            # stack the 2 images together side by side
            stacked_img = stack_img(og_tex, horizontal_flip, "RIGHT")

            # flip the stacked img about the bottom side
            vertical_flip = flip_img(stacked_img, "HORIZONTAL")

            # stack the stacked img and flipped img top n bottom
            stacked_img2 = stack_img(stacked_img, vertical_flip, "TOP")

            # smudge the internal boundaries of the final stacked img
            # by copying a patch of (block_size x block_size) from a random location
            # continuous_tex = smudge_boundaries(stacked_img2, block_size)

            continuous_tex = stacked_img2

            if display_tex:
                cv2.imshow("original tex", og_tex)
                cv2.imshow("continuous tex", continuous_tex)
                cv2.waitKey(0)

            if save_tex:
                generated_img_name = "continuous-"+img_filename+".png"
                cv2.imwrite(os.path.join(out_dir, generated_img_name), continuous_tex)


if __name__ == "__main__":

    img_dir = "..//data\\blender_data\\landscape\\textures\\"
    block_size = 50
    display_texture = False
    save_texture = True
    out_dir = None

    continuous_texture(img_dir, block_size, display_texture, save_texture, out_dir)