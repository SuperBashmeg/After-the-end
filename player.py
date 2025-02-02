from config import *

class Player:
    def __init__(self, x, y, width=50, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_width = width
        self.original_height = height
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.on_ground = False
        self.coyote_timer = 0
        self.coyote_time = 0.1
        self.jump_buffer = False
        self.channel = 0
        self.freeze = False
        self.changing_level = False
        self.trail = []  # List to store previous positions
        self.max_trail_length = 20  # Maximum length of the trail
        self.death_effect_active = False
        self.death_effect_timer = 0
        self.death_effect_velocity = 2000
        self.spawn_position = pygame.Vector2(x, y)
        self.squish_timer = 0
        self.squish_duration = 0.2  # Duration of the squish effect
        self.particles = []
        self.draw_player = True

    def get_clipped_position(self, object):
        player_position = [
            (self.x, self.y),  # top left
            (self.x + self.width, self.y),  # top right
            (self.x, self.y + self.height),  # bottom left
            (self.x + self.width, self.y + self.height),  # bottom right

            (self.x, self.y + self.height / 2),  # left middle
            (self.x + self.width / 2, self.y + self.height),  # bottom middle
            (self.x + self.width, self.y + self.height / 2),  # right middle
            (self.x + self.width / 2, self.y),  # top middle

            (self.x + self.width / 2, self.y + self.height / 2)  # center
        ]
        platform_corners = [
            (object.x, object.y),  # top left
            (object.x + object.width, object.y),  # top right
            (object.x, object.y + object.height),  # bottom left
            (object.x + object.width, object.y + object.height)  # bottom right
        ]
        clipped_position = [
            False,  # top left 0
            False,  # top right 1
            False,  # bottom left 2
            False,  # bottom right 3
            False,  # left middle 4
            False,  # bottom middle 5
            False,  # right middle 6
            False,  # top middle 7
            False,  # center 8
        ]
        n_clipped = 0
        for i in range(9):
            if platform_corners[0][0] <= player_position[i][0] <= platform_corners[1][
                0] and platform_corners[0][1] <= player_position[i][1] <= platform_corners[2][1]:
                clipped_position[i] = True
                n_clipped += 1
        return clipped_position, n_clipped

    def get_clipped_positions_in_spike(self, object):
        player_position = [
            (self.x, self.y),  # top left
            (self.x + self.width, self.y),  # top right
            (self.x, self.y + self.height),  # bottom left
            (self.x + self.width, self.y + self.height),  # bottom right

            (self.x, self.y + self.height / 2),  # left middle
            (self.x + self.width / 2, self.y + self.height),  # bottom middle
            (self.x + self.width, self.y + self.height / 2),  # right middle
            (self.x + self.width / 2, self.y),  # top middle

            (self.x + self.width / 2, self.y + self.height / 2)  # center
        ]
        spike_corners = [
            (object.x - object.width/2, object.y+object.height/3),  # top left
            (object.x + object.width/2, object.y+object.height/3),  # top right
            (object.x - object.width/2, object.y-object.height/2),  # bottom left
            (object.x + object.width/2, object.y-object.height/2),  # bottom right
        ]
        clipped_position = [
            False,  # top left 0
            False,  # top right 1
            False,  # bottom left 2
            False,  # bottom right 3
            False,  # left middle 4
            False,  # bottom middle 5
            False,  # right middle 6
            False,  # top middle 7
            False,  # center 8
        ]
        n_clipped = 0
        for i in range(9):
            if (spike_corners[0][0] <= player_position[i][0] <= spike_corners[1][0] and
                    spike_corners[0][1] >= player_position[i][1] >= spike_corners[2][1]):
                clipped_position[i] = True
                n_clipped += 1
        return clipped_position, n_clipped

    def get_collisions(self, level):
        platforms = level.platforms
        spikes = level.spikes
        collisions = {"Left":[],"Down":[],"Right":[],"Up":[], "Center":[], "Star":[]}
        player_position = [
            (self.x, self.y),  # top left 0
            (self.x + self.width, self.y),  # top right 1
            (self.x, self.y + self.height),  # bottom left 2
            (self.x + self.width, self.y + self.height),  # bottom right 3

            (self.x, self.y + self.height / 2),  # left middle 4
            (self.x + self.width / 2, self.y + self.height),  # bottom middle 5
            (self.x + self.width, self.y + self.height / 2),  # right middle 6
            (self.x + self.width / 2, self.y),  # top middle 7

            (self.x + self.width / 2, self.y + self.height / 2)  # center 8
        ]
        for platform in platforms:
            if not self.channel in platform.channels:
                continue
            platform_corners = [
                (platform.x, platform.y),  # top left
                (platform.x + platform.width, platform.y),  # top right
                (platform.x, platform.y + platform.height),  # bottom left
                (platform.x + platform.width, platform.y + platform.height)  # bottom right
            ]
            clipped_position, n_clipped = self.get_clipped_position(platform)
            if clipped_position[8]:
                collisions["Center"].append(platform)
            elif player_position[0][0] < platform_corners[1][0] and player_position[1][0] > platform_corners[0][0] and platform.y < self.y + self.height + 0.001 < platform.y + platform.height and platform.y - self.y > 10 and platform.collisions["down"]:
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

        clipped_position, star_clipped_amount = self.get_clipped_position(level.star)
        if star_clipped_amount > 0:
            collisions["Star"].append(level.star)

        for spike in spikes:
            if not self.channel in spike.channels:
                continue
            clipped_position, n_clipped = self.get_clipped_positions_in_spike(spike)
            if n_clipped > 0:
                self.death()

        return collisions


    def death_effect(self, dt):
        # if abs(self.spawn_position.x-self.x) < 100 and abs(self.spawn_position.y-self.y) < 100:
        #     print("Respawn")
        #     self.death_effect_active = False
        #     self.respawn(self.spawn_position.x, self.spawn_position.y)
        #     return
        if self.death_effect_timer <= 0:
            print("Respawn")
            self.death_effect_active = False
            self.respawn(self.spawn_position.x, self.spawn_position.y)
            return
        self.death_effect_timer -= dt
        # direction = pygame.Vector2(self.spawn_position.x-self.x, self.spawn_position.y-self.y).normalize()
        # self.y += self.death_effect_velocity * direction.y * dt
        # self.x += self.death_effect_velocity * direction.x * dt



    def death(self):
        self.death_effect_timer = 1
        self.death_effect_active = True
        self.freeze = True
        self.draw_player = False
        for particle in range(25):
            size = random.randint(1, 10)
            random_x = random.uniform(self.x, self.x+self.width)
            random_y = random.uniform(self.y, self.y+self.height)
            particle = Particle((random_x, random_y), size, size, (255, 0, 0), 0.01, [random.uniform(-50, 50), random.uniform(-50, 50)], random.uniform(0, 360), random.uniform(-10, 10), 0.5, 0.25)
            self.particles.append(particle)


    def respawn(self, x, y):
        for particle in range(25):
            size = random.randint(1, 10)
            random_x = random.uniform(x, x + self.width)
            random_y = random.uniform(y, y + self.height)
            particle = Particle((random_x, random_y), size, size, (255, 0, 0), 2, [random.uniform(-25, 25), random.uniform(-25, 25)], random.uniform(0, 360), random.uniform(-10, 10), 0.5, 0.1)
            self.particles.append(particle)
        self.x = x
        self.y = y
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = False
        self.channel = 0
        self.freeze = False
        self.draw_player = True
        self.changing_level = False
        self.trail = []  # List to store previous positions
        death_event = pygame.event.Event(pygame.USEREVENT + 1)
        pygame.event.post(death_event)  # Death event


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
                self.velocity.y = -self.velocity.y/2
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
            if self.velocity.x > 0:
                self.acceleration.x = -player_speed * 10
        elif move_right and not move_left:
            if self.on_ground:
                self.acceleration.x = player_speed
            else:
                self.acceleration.x = player_speed * air_acceleration_factor
            if self.velocity.x < 0:
                self.acceleration.x = player_speed * 10
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
        if self.on_ground or self.coyote_timer > 0:
            self.velocity.y = jump_height
            self.jump_buffer = False
            self.coyote_timer = 0
            self.squish_timer = self.squish_duration
            self.height = self.original_height * 0.8  # Squish height
            self.width = self.original_width * 1.2

    def update_squish(self, dt):
        if self.squish_timer > 0:
            self.squish_timer -= dt
            squish_factor = self.squish_timer / self.squish_duration
            self.height = self.original_height * (1.1 + 0.2 * squish_factor)
            self.y = self.y - self.original_height * 0.1 * squish_factor
            self.width = self.original_width * (0.9 - 0.2 * squish_factor)
        else:
            self.height = self.original_height
            self.width = self.original_width

    def update(self, dt, level, move_left=False, move_right=False):
        if self.death_effect_active:
            self.death_effect(dt)
        if not self.freeze:
            if self.y+self.height/2 > 720:
                self.death()
                return
            elif self.y+self.height/2 < 0:
                self.death()
                return
            elif self.x+self.width/2 > 1280:
                self.death()
                return
            elif self.x+self.width/2 < 0:
                self.death()
                return
            collisions = self.get_collisions(level)
            if len(collisions["Down"]) > 0:
                if not self.on_ground:
                    for i in range(10):
                        if self.velocity.y > 0:
                            size = random.randint(1, 5)*self.velocity.y/333
                            velocity_multiplier = self.velocity.y/333
                            random_x = random.uniform(self.x, self.x+self.width)
                            particle = Particle((random_x, self.y+self.height-8), size, size, (255, 0, 0), 0, [random.uniform(-25, 25)*velocity_multiplier, random.uniform(5, 25)*velocity_multiplier], 0, 0)
                            self.particles.append(particle)
                self.on_ground = True
                self.coyote_timer = self.coyote_time
            else:
                self.on_ground = False
                self.coyote_timer -= dt

            if self.on_ground:
                self.acceleration.y = 0
                self.velocity.y = 0
            else:
                self.acceleration.y = gravity

            self.__unclip(collisions)

            self.move(dt, collisions, move_left, move_right)
            if self.jump_buffer:
                self.jump()
            self.velocity += self.acceleration * dt

            if collisions["Star"]:
                self.changing_level = True
                self.freeze = True

            self.y += self.velocity.y * dt

            if (not move_left and not move_right) or (move_right and move_left):
                self.friction()
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.destroyed:
                self.particles.remove(particle)
            # Update the trail
        if self.draw_player:
            self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        if len(self.trail) > 0 and not self.draw_player:
            self.trail.pop(0)

        self.update_squish(dt)

    def draw(self, screen):
        # Draw the trail
        for particle in self.particles[:]:
            particle.draw(screen)
        for i, (x, y) in enumerate(self.trail):
            alpha = int(50 * (i + 1) / len(self.trail))
            trail_color = (255, 0, 0, alpha)
            trail_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            trail_surface.fill(trail_color)
            screen.blit(trail_surface, (x, y))

        # Draw the player
        if self.draw_player:
            pygame.draw.rect(screen, (255, 0, 0, 255), (self.x, self.y, self.width, self.height), 0, 4)