import random

def play_game():
    print("Welcome to the Number Guessing Game!")
    print("I am thinking of a number between 1 and 100.")
    
    # The computer selects a random secret number
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    
    print(f"You have {max_attempts} attempts to guess it. Good luck!\n")
    
    # Game Loop
    while attempts < max_attempts:
        user_input = input(f"Attempt {attempts + 1}/{max_attempts} - Enter your guess: ").strip()
        
        # Validate that the user actually entered a number
        if not user_input.isdigit():
            print("Invalid input. Please enter a valid number.\n")
            continue
            
        guess = int(user_input)
        attempts += 1
        
        # Check the user's guess against the secret number
        if guess < secret_number:
            print("Too low! Try a higher number.\n")
        elif guess > secret_number:
            print("Too high! Try a lower number.\n")
        else:
            print(f"🎉 Congratulations! You guessed the number in {attempts} attempts!")
            return  # End the game because they won
            
    # If the loop finishes, the player ran out of turns
    print(f"😭 Game Over! You ran out of attempts. The number was {secret_number}.")

# Run the game
if __name__ == "__main__":
    play_game()
  






import cv2
import numpy as np
import random

# Initialize webcam
cap = cv2.VideoCapture(0)

# Game variables
score = 0
lives = 3
game_over = False

# Ball variables (X, Y position and speed)
ball_x = random.randint(50, 590)
ball_y = 0
ball_radius = 20
ball_speed = 10

print("Game Started! Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Error: Could not read from webcam.")
        break

    # Flip the frame horizontally for a natural mirror effect
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # 1. Background Subtraction to find the moving object (your hand)
    # Convert frame to grayscale and blur it to reduce noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    # Initialize static background on the first frame
    if 'static_back' not in locals():
        static_back = blurred
        continue

    # Find the difference between current frame and static background
    diff_frame = cv2.absdiff(static_back, blurred)
    _, thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find outlines (contours) of the moving object
    contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest moving object is the player's hand
    player_x, player_y, player_w, player_h = 0, 0, 0, 0
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 5000:  # Filter out tiny movements
            player_x, player_y, player_w, player_h = cv2.boundingRect(largest_contour)
            # Draw a green bounding box around your hand
            cv2.rectangle(frame, (player_x, player_y), (player_x + player_w, player_y + player_h), (0, 255, 0), 2)

    # 2. Game Logic
#     if not game_over:
#         # Move the falling ball
#         ball_y += ball_speed

#         # Check if ball hits the bottom
#         if ball_y > height:
#             lives -= 1
#             ball_y = 0
#             ball_x = random.randint(50, width - 50)
#             ball_speed = random.randint(8, 15)
#             if lives <= 0:
#                 game_over = True

#         # Check Collision: Did the ball hit the player's bounding box?
#         if player_w > 0:  # If a hand is detected
#             if (player_x < ball_x < player_x + player_w) and (player_y < ball_y < player_y + player_h):
#                 score += 1
#                 ball_y = 0
#                 ball_x = random.randint(50, width - 50)
#                 ball_speed = min(ball_speed + 1, 25)  # Make it faster and harder

#     # 3. Drawing the UI & Visual Elements
#     # Draw the falling ball (Blue circle)
#     if not game_over:
#         cv2.circle(frame, (ball_x, ball_y), ball_radius, (255, 0, 0), -1)

#     # Draw Score and Lives on screen
#     cv2.putText(frame, f"Score: {score}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
#     cv2.putText(frame, f"Lives: {lives}", (width - 150, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     # Draw Game Over Text
#     if game_over:
#         cv2.putText(frame, "GAME OVER", (width // 4, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
#         cv2.putText(frame, "Press 'r' to Restart", (width // 4, (height // 2) + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#     # Show the game window
#     cv2.imshow("OpenCV Catching Game", frame)

#     # 4. Keyboard Controls
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):  # Press 'q' to quit
#         break
#     elif key == ord('r') and game_over:  # Press 'r' to restart
#         score = 0
#         lives = 3
#         game_over = False
#         ball_y = 0
#         del static_back  # Reset background reference

# # Cleanup
# cap.release()
# cv2.destroyAllWindows()


import cv2
import numpy as np
import random
import time

# Initialize webcam
cap = cv2.VideoCapture(0)

# Game State
score = 0
game_duration = 30  # 30-second game blitz
start_time = time.time()

# Target (Green Goblin drone)
target_radius = 30
target_x = random.randint(50, 590)
target_y = random.randint(50, 430)

# Web effect variables
web_active = False
web_timer = 0
web_origin = (0, 0)
web_target = (0, 0)

print("Spidey Web Shooter Simulator Started! Press 'q' to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Mirror the frame for intuitive control
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    
    # Calculate remaining time
    elapsed_time = time.time() - start_time
    time_left = max(0, int(game_duration - elapsed_time))
    
    # 1. Computer Vision: Motion and Gesture Processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    
    if 'bg_frame' not in locals():
        bg_frame = blurred
        continue

    # Detect hand movement/presence using frame difference
    diff = cv2.absdiff(bg_frame, blurred)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    spidey_hand_detected = False
    hand_center = (0, 0)

    if contours and time_left > 0:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 4000:
            # Get bounding box and center of the player's hand
            x, y, w, h = cv2.boundingRect(largest)
            hand_center = (x + w // 2, y + h // 2)
            spidey_hand_detected = True
            
            # Draw a stylized web reticle over your hand
            cv2.circle(frame, hand_center, 15, (0, 0, 255), 2)
            cv2.line(frame, (hand_center[0]-25, hand_center[1]), (hand_center[0]+25, hand_center[1]), (0, 0, 255), 1)
            cv2.line(frame, (hand_center[0], hand_center[1]-25), (hand_center[0], hand_center[1]+25), (0, 0, 255), 1)

            # Gesture Logic: Trigger web shoot if hand moves fast or expands sharply
            # (Simulates throwing your hand forward instantly)
            if w > 180 and not web_active:
                web_active = True
                web_timer = 5  # Show the web line for 5 video frames
                web_origin = hand_center
                web_target = (target_x, target_y)
                
                # Check if web hits the villain drone
                distance = np.sqrt((hand_center[0] - target_x)**2 + (hand_center[1] - target_y)**2)
                if distance < (target_radius + 60):  # Generous hitbox for fun
                    score += 1
                    # Spawn next target
                    target_x = random.randint(50, width - 50)
                    target_y = random.randint(50, height - 100)

    # 2. Rendering Visual Elements
    if time_left > 0:
        # Draw the Villain Target (Red & Green energy orb)
        cv2.circle(frame, (target_x, target_y), target_radius, (0, 128, 0), -1)
        cv2.circle(frame, (target_x, target_y), target_radius - 10, (0, 0, 255), -1)
        cv2.putText(frame, "VILLAIN", (target_x - 30, target_y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # Draw the Web String if fired
        if web_active and web_timer > 0:
            # Draw multiple web lines converging to look like web strands
            cv2.line(frame, web_origin, web_target, (255, 255, 255), 4)
            cv2.line(frame, (web_origin[0]-10, web_origin[1]), web_target, (240, 240, 240), 1)
            cv2.line(frame, (web_origin[0]+10, web_origin[1]), web_target, (240, 240, 240), 1)
            web_timer -= 1
        else:
            web_active = False
    else:
        # Game Over Screen
        cv2.putText(frame, "TIME'S UP, SPIDEY!", (width // 5, height // 2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
        cv2.putText(frame, f"Final Score: {score} Targets Caught", (width // 4, height // 2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'r' to Swing Again", (width // 4, height // 2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Heads-Up Display (HUD)
    cv2.putText(frame, f"Score: {score}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f"Time: {time_left}s", (width - 160, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display game window
    cv2.imshow("Spider-Man Web Shooter Simulator", frame)

    # Keyboard Handlers
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r') and time_left == 0:
        # Restart game state
        score = 0
        start_time = time.time()
        del bg_frame

cap.release()
cv2.destroyAllWindows()
