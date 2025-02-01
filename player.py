from config import *

class Player:
    def __init__(self, x, y, width=50, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.on_ground = False
        self.freeze = False

    def get_collisions(self, platforms):
        collisions = {"Left":[],"Down":[],"Right":[],"Up":[]}
        player_position = [
            (self.x, self.y),  # top left
            (self.x + self.width, self.y),  # top right
            (self.x, self.y + self.height),  # bottom left
            (self.x + self.width, self.y + self.height),  # bottom right

            (self.x, self.y + self.height / 2),  # left middle
            (self.x + self.width / 2, self.y + self.height),  # bottom middle
            (self.x + self.width, self.y + self.height / 2),  # right middle
            (self.x + self.width / 2, self.y)  # top middle
        ]
        for platform in platforms:
            platform_corners = [
                (platform.x, platform.y),  # top left
                (platform.x + platform.width, platform.y),  # top right
                (platform.x, platform.y + platform.height),  # bottom left
                (platform.x + platform.width, platform.y + platform.height)  # bottom right
            ]
            clipped_position = [
                False, # top left 0
                False, # top right 1
                False, # bottom left 2
                False, # bottom right 3
                False, # left middle 4
                False, # bottom middle 5
                False, # right middle 6
                False  # top middle 7
            ]
            n_clipped = 0
            for i in range(8):
                if player_position[i][0] >= platform_corners[0][0] and player_position[i][0] <= platform_corners[1][0] and player_position[i][1] >= platform_corners[0][1] and player_position[i][1] <= platform_corners[2][1]:
                    clipped_position[i] = True
                    n_clipped += 1

            #Down check
            if (clipped_position[2] or clipped_position[3] or clipped_position[5]) and not clipped_position[4] and not clipped_position[6] and n_clipped <= 3 and platform.collisions["down"]:
                collisions["Down"].append(platform)
            #Up check
            elif (clipped_position[0] or clipped_position[1] or clipped_position[7]) and not clipped_position[4] and not clipped_position[6] and n_clipped <= 3 and platform.collisions["up"]:
                 collisions["Up"].append(platform)
            #Left check
            elif (clipped_position[0] or clipped_position[2] or clipped_position[4]) and not clipped_position[5] and not clipped_position[7] and n_clipped <= 3 and platform.collisions["left"]:
                collisions["Left"].append(platform)
            #Right check
            elif (clipped_position[1] or clipped_position[3] or clipped_position[6]) and not clipped_position[5] and not clipped_position[7] and n_clipped <= 3 and platform.collisions["right"]:
                collisions["Right"].append(platform)

        return collisions

    def __unclip(self, collisions):
        if len(collisions["Down"]) > 0:
            biggest_y = collisions["Down"][0].y
            for i in collisions["Down"]:
                if i.y > biggest_y:
                    biggest_y = i.y
            if self.y + self.height > biggest_y:
                self.on_ground = True
                self.y = biggest_y - self.height
                self.acceleration.y = 0
                self.velocity.y = 0

        if len(collisions["Up"]) > 0:
            biggest_y = collisions["Up"][0].y + collisions["Up"][0].height
            for i in collisions["Up"]:
                if i.y + i.height > biggest_y:
                    biggest_y = i.y + i.height
            if self.y < biggest_y:
                self.y = biggest_y
                self.velocity.y = 0
                self.acceleration.y = 0

        if len(collisions["Left"]) > 0:
            biggest_x = collisions["Left"][0].x+collisions["Left"][0].width
            for i in collisions["Left"]:
                if i.x+i.width < biggest_x:
                    biggest_x = i.x+i.width

            if self.x < biggest_x:
                self.x = biggest_x
                self.acceleration.x = 0
                self.velocity.x = 0

        if len(collisions["Right"]) > 0:
            biggest_x = collisions["Right"][0].x-self.width
            for i in collisions["Right"]:
                if i.x-self.width > biggest_x:
                    biggest_x = i.x-self.width
            if self.x > biggest_x:
                self.x = biggest_x
                self.acceleration.x = 0
                self.velocity.x = 0

    def move(self, dt, collisions, move_left, move_right):
        if move_left and not move_right and len(collisions["Left"]) == 0:
            if self.on_ground:
                self.acceleration.x = -player_speed
            else:
                self.acceleration.x = -player_speed * air_acceleration_factor
        elif move_right and not move_left:
            if self.on_ground:
                self.acceleration.x = player_speed
            else:
                self.acceleration.x = player_speed * air_acceleration_factor
            print(self.acceleration.x, self.on_ground)
        else:
            self.acceleration.x = 0


        self.velocity += self.acceleration * dt
        self.x += self.velocity.x * dt

        self.__unclip(collisions)
        if self.velocity.x < 0:
            self.velocity.x = max(self.velocity.x, -player_speed)
        elif self.velocity.x > 0:
            self.velocity.x = min(self.velocity.x, player_speed)


    def friction(self):
        if self.on_ground:
            self.velocity.x *= ground_friction
        else:
            self.velocity.x *= friction

    def jump(self):
        if self.on_ground:
            self.velocity.y = jump_height

    def update(self, dt, platforms, move_left=False, move_right=False, spacebar=False):
        if not self.freeze:
            collisions = self.get_collisions(platforms)
            print(collisions)
            if len(collisions["Down"]) > 0:
                self.on_ground = True
            else:
                self.on_ground = False


            if self.on_ground:
                self.acceleration.y = 0
                self.velocity.y = 0
            else:
                self.acceleration.y = gravity

            self.__unclip(collisions)

            self.move(dt, collisions, move_left, move_right)
            if spacebar:
                self.jump()
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.acceleration.y = gravity
            self.velocity += self.acceleration * dt


            self.y += self.velocity.y * dt

            if (not move_left and not move_right) or (move_right and move_left):
                self.friction()



    def draw(self, screen):
        pygame.draw.rect(screen, "red", (self.x, self.y, self.width, self.height))