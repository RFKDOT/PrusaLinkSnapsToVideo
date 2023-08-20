import os
import cv2
import glob
import time

def list_projects_in_png():
    # Escanear el directorio 'media/png/' y obtener una lista de todos los archivos
    all_images = glob.glob("media/png/*.png")

    # Agrupar imágenes por proyecto
    projects = {}
    for image in all_images:
        project_name = image.split('/')[1].split('_@_')[0]
        if project_name in projects:
            projects[project_name].append(image)
        else:
            projects[project_name] = [image]

    return projects

def select_project(projects):
    # Mostrar al usuario una lista de proyectos
    print("\nList of Projects:", flush=True)
    for idx, project in enumerate(projects.keys(), 1):
        print(f"{idx}. {project}")

    # Permitir que el usuario seleccione un proyecto
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
    # Get the frame dimensions from the first image
    frame = cv2.imread(images[0])
    h, w, l = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 1.0 / duration_per_image, (w, h))

    # Write each frame to the video
    for image_path in images:
        img = cv2.imread(image_path)
        out.write(img)

    out.release()

def main_script():
    projects = list_projects_in_png()
    selected_project_name, selected_project_images = select_project(projects)

    # Sort images by the timestamp in their name
    sorted_images = sorted(selected_project_images, key=lambda x: int(x.split('_')[-1].split('.')[0]))

    # Ask user for duration of each snapshot or the total video duration
    choice = input("\nDo you want to specify the duration for each snapshot or for the total video?\n1. Each snapshot\n2. Total video\nChoose (1/2): ")

    if choice == "1":
        duration_per_image = float(input("Enter the duration for each snapshot in seconds (e.g. 0.5): "))
        total_duration = len(sorted_images) * duration_per_image
    else:
        total_duration = float(input("Enter the total video duration in seconds (e.g. 30): "))
        duration_per_image = total_duration / len(sorted_images)

    print(f"Duration per image {duration_per_image}\n", flush=True)
    print(f"Total duration {total_duration}\n", flush=True)

    # Create video
    output_path = f"media/mp4/{selected_project_name}_{time.time()}.mp4"
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