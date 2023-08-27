import os
import cv2
import glob
import time
from datetime import datetime

def list_projects_in_png():
    all_images = glob.glob("media/png/*.png")

    projects = {}
    for image in all_images:
        project_name = os.path.basename(image).split('_@_')[0]
        if project_name in projects:
            projects[project_name].append(image)
        else:
            projects[project_name] = [image]

    return projects

def select_project(projects):
    print("\nList of Projects:", flush=True)
    for idx, project in enumerate(projects.keys(), 1):
        print(f"{idx}. {project}")

    while True:
        try:
            selection = int(input("\nSelect a project by number: "))
            if 1 <= selection <= len(projects):
                project_name = list(projects.keys())[selection - 1]
                return project_name, projects[project_name]
            else:
                print("Invalid selection. Please choose a valid number.", flush=True)
        except ValueError:
            print("Please enter a valid number.", flush=True)

def create_video_from_images(images, duration_per_image, output_path):
    frame = cv2.imread(images[0])
    h, w, l = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 1.0 / duration_per_image, (w, h))

    for image_path in images:
        img = cv2.imread(image_path)
        out.write(img)

    out.release()

def main_script():
    projects = list_projects_in_png()
    selected_project_name, selected_project_images = select_project(projects)

    sorted_images = sorted(selected_project_images, key=lambda x: int(x.split('_')[-1].split('.')[0]))

    # choice = input("\nDo you want to specify the duration for each snapshot or for the total video?\n1. Each snapshot\n2. Total video\nChoose (1/2): ")

    # if choice == "1":
    #     duration_per_image = float(input("Enter the duration for each snapshot in seconds (e.g. 0.5): "))
    #     total_duration = len(sorted_images) * duration_per_image
    # else:
    #     total_duration = float(input("Enter the total video duration in seconds (e.g. 30): "))
    #     duration_per_image = total_duration / len(sorted_images)

    # print(f"Duration per image {duration_per_image}\n", flush=True)
    # print(f"Total duration {total_duration}\n", flush=True)

    duration_per_image = 0.3

    # Create video
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = f"media/mp4/{selected_project_name}_{date}.mp4"
    create_video_from_images(sorted_images, duration_per_image, output_path)
    print(f"\nVideo saved as {output_path}", flush=True)

    # Ask user if they want to delete the images used for the video
    # delete_choice = input("\nDo you want to delete the images used to create the video? (yes/no): ")
    # if delete_choice.lower() == "yes":
    #     for img in sorted_images:
    #         os.remove(img)
    #     print("\nImages deleted successfully.")

# The main_script function encapsulates the entire process, but we won't call it here due to the input() limitation.
main_script()