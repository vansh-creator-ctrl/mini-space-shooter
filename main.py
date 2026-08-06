import math
import random
import asyncio
import pygame

# --- Configuration & Constants ---
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
FPS = 60
SCORE_PER_LEVEL = 150

# Color Palette
CYAN = (0, 230, 230)
GOLD = (255, 210, 0)
RED = (230, 50, 60)
GREEN = (60, 220, 120)
PURPLE = (190, 90, 255)
WHITE = (245, 245, 255)

BOOSTER_COLORS = {
    "rapid": GOLD,
    "shield": (0, 200, 255),
    "multi": PURPLE,
    "life": GREEN,
}

BOOSTER_DURATIONS = {
    "rapid": 360,
    "multi": 360,
    "shield": 300,
}

THEMES = [
    {
        "top": (8, 8, 20),
        "bottom": (18, 14, 40),
        "nebula": [(100, 60, 160, (60, 40, 160)), (480, 500, 130, (30, 120, 160))],
        "planet": (520, 90, 34, (70, 90, 160)),
    },
    {
        "top": (6, 14, 30),
        "bottom": (30, 10, 45),
        "nebula": [(500, 120, 150, (160, 40, 120)), (60, 520, 110, (40, 60, 160))],
        "planet": (70, 600, 46, (150, 60, 140)),
    },
    {
        "top": (10, 6, 25),
        "bottom": (45, 12, 20),
        "nebula": [(150, 550, 160, (200, 60, 40)), (500, 100, 100, (150, 40, 30))],
        "planet": (540, 620, 38, (200, 90, 40)),
    },
]


# --- Asset Builders ---
def create_ship_surface():
    surf = pygame.Surface((44, 50), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (0, 160, 255, 120), (12, 34, 20, 16))
    pygame.draw.polygon(surf, (0, 150, 190), [(10, 26), (0, 44), (16, 36)])
    pygame.draw.polygon(surf, (0, 150, 190), [(34, 26), (44, 44), (28, 36)])
    pygame.draw.polygon(surf, (0, 200, 230), [(10, 26), (2, 40), (14, 34)])
    pygame.draw.polygon(surf, (0, 200, 230), [(34, 26), (42, 40), (30, 34)])
    pygame.draw.polygon(surf, (0, 235, 235), [(22, 2), (10, 34), (22, 28), (34, 34)])
    pygame.draw.polygon(surf, (150, 255, 255), [(22, 2), (17, 22), (22, 20), (27, 22)])

    pygame.draw.ellipse(surf, (30, 40, 60), (17, 9, 10, 14))
    pygame.draw.ellipse(surf, (220, 255, 255), (18, 10, 8, 10))
    pygame.draw.ellipse(surf, (255, 255, 255), (19, 11, 3, 4))
    pygame.draw.line(surf, (200, 255, 255), (12, 30), (5, 40), 2)
    pygame.draw.line(surf, (200, 255, 255), (32, 30), (39, 40), 2)

    pygame.draw.circle(surf, (255, 80, 80), (4, 41), 2)
    pygame.draw.circle(surf, (80, 255, 120), (40, 41), 2)
    return surf


def create_alien_surface(variant=0):
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    palette = [(220, 40, 50), (220, 120, 30), (150, 60, 220)]
    color = palette[variant % 3]
    dark = tuple(max(0, c - 60) for c in color)
    light = tuple(min(255, c + 50) for c in color)

    pygame.draw.ellipse(surf, color, (3, 4, 26, 20))
    pygame.draw.ellipse(surf, light, (6, 6, 14, 8))
    pygame.draw.polygon(surf, dark, [(3, 13), (0, 27), (9, 19)])
    pygame.draw.polygon(surf, dark, [(29, 13), (32, 27), (23, 19)])
    pygame.draw.circle(surf, (255, 220, 0), (11, 12), 3)
    pygame.draw.circle(surf, (255, 220, 0), (21, 12), 3)
    pygame.draw.circle(surf, (30, 20, 0), (11, 12), 1)
    pygame.draw.circle(surf, (30, 20, 0), (21, 12), 1)
    return surf


def create_laser_surface(color=(255, 220, 0)):
    surf = pygame.Surface((6, 16), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (0, 0, 6, 16), border_radius=3)
    pygame.draw.rect(surf, (255, 255, 255), (2, 0, 2, 16), border_radius=2)
    return surf


def create_booster_icon(kind, font):
    surf = pygame.Surface((26, 26), pygame.SRCALPHA)
    color = BOOSTER_COLORS[kind]
    pygame.draw.circle(surf, (*color, 70), (13, 13), 13)
    pygame.draw.circle(surf, color, (13, 13), 10)
    pygame.draw.circle(surf, WHITE, (13, 13), 10, 2)

    labels = {"rapid": "R", "shield": "S", "multi": "M", "life": "+"}
    text_surf = font.render(labels[kind], True, (20, 20, 20))
    surf.blit(text_surf, (13 - text_surf.get_width() // 2, 13 - text_surf.get_height() // 2))
    return surf


def build_asteroid_surface(seed):
    rng = random.Random(seed)
    radius = rng.randint(14, 26)
    surf = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
    center = radius + 2

    base = rng.choice([(120, 110, 100), (90, 95, 110), (110, 90, 80)])
    dark = tuple(max(0, c - 45) for c in base)

    points = []
    num_verts = rng.randint(8, 11)
    for i in range(num_verts):
        angle = (2 * math.pi / num_verts) * i
        dist = radius * rng.uniform(0.65, 1.0)
        points.append((center + math.cos(angle) * dist, center + math.sin(angle) * dist))

    pygame.draw.polygon(surf, base, points)
    pygame.draw.polygon(surf, dark, points, 2)

    for _ in range(rng.randint(2, 4)):
        crater_x = center + rng.uniform(-radius * 0.4, radius * 0.4)
        crater_y = center + rng.uniform(-radius * 0.4, radius * 0.4)
        pygame.draw.circle(surf, dark, (int(crater_x), int(crater_y)), rng.randint(2, 4))

    return surf, radius


def draw_background(theme):
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Gradient setup
    for y in range(SCREEN_HEIGHT):
        progress = y / SCREEN_HEIGHT
        color = tuple(
            int(theme["top"][i] + (theme["bottom"][i] - theme["top"][i]) * progress)
            for i in range(3)
        )
        pygame.draw.line(surf, color, (0, y), (SCREEN_WIDTH, y))

    # Render nebulas
    for nx, ny, nr, ncol in theme["nebula"]:
        for r in range(nr, 0, -6):
            alpha = int(26 * (1 - r / nr))
            blob = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(blob, (*ncol, alpha), (r, r), r)
            surf.blit(blob, (nx - r, ny - r), special_flags=pygame.BLEND_RGBA_ADD)

    # Render planet
    px, py, pr, pcol = theme["planet"]
    shade = tuple(max(0, c - 70) for c in pcol)
    highlight = tuple(min(255, c + 60) for c in pcol)

    pygame.draw.circle(surf, (*pcol, 255), (px, py), pr)
    pygame.draw.circle(surf, (*shade, 160), (px + pr // 4, py + pr // 4), pr)
    pygame.draw.circle(surf, (*highlight, 90), (px - pr // 3, py - pr // 3), pr // 2)

    ring = pygame.Surface((pr * 3, pr), pygame.SRCALPHA)
    pygame.draw.ellipse(ring, (*highlight, 60), (0, 0, pr * 3, pr), 3)
    surf.blit(ring, (px - pr * 3 // 2, py - pr // 2))

    return surf


def build_vignette():
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    max_radius = math.hypot(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    steps = 40
    for i in range(steps):
        t = i / steps
        radius = max_radius * (1 - t * 0.35)
        alpha = int(70 * t)
        pygame.draw.circle(
            surf,
            (0, 0, 10, alpha),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            int(radius),
            width=max(1, int(max_radius / steps) + 2)
        )
    return surf


# --- Entity Classes ---
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 6
        self.rect = pygame.Rect(x + 4, y + 4, 36, 40)

    def move(self, dx):
        self.x = max(0, min(SCREEN_WIDTH - 44, self.x + dx * self.speed))
        self.rect.topleft = (self.x + 4, self.y + 4)


class Asteroid:
    def __init__(self):
        self.image, self.size = build_asteroid_surface(random.randint(0, 99999))
        self.x = random.randint(-40, SCREEN_WIDTH + 40)
        self.y = random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
        self.vy = random.uniform(0.3, 0.9)
        self.vx = random.uniform(-0.3, 0.3)
        self.spin = random.uniform(-0.6, 0.6)
        self.angle = random.uniform(0, 360)

    def update(self):
        self.y += self.vy
        self.x += self.vx
        self.angle = (self.angle + self.spin) % 360
        if self.y > SCREEN_HEIGHT + 40:
            self.y = -40
            self.x = random.randint(-40, SCREEN_WIDTH + 40)


class Particle:
    def __init__(self, x, y, vx, vy, life, color, size, kind="dot"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.color = color
        self.size = size
        self.kind = kind

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.life -= 1


# --- Main Game Engine ---
class SpaceGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 20)
        self.font_sm = pygame.font.SysFont("arial", 15)
        self.font_bg = pygame.font.SysFont("arial", 48, bold=True)

        # Pre-render surfaces
        self.ship_img = create_ship_surface()
        self.aliens = [create_alien_surface(i) for i in range(3)]
        self.laser_img = create_laser_surface()
        self.laser_multi_img = create_laser_surface((0, 200, 255))
        self.booster_imgs = {k: create_booster_icon(k, self.font_sm) for k in BOOSTER_COLORS}
        self.vignette = build_vignette()
        self.backgrounds = [draw_background(t) for t in THEMES]

        self.stars = self._init_starfield()
        self.asteroids = [Asteroid() for _ in range(7)]
        self.comets = []
        self.comet_timer = 0

        self.reset()

    def reset(self):
        self.player = Player(SCREEN_WIDTH // 2 - 22, SCREEN_HEIGHT - 80)
        self.bullets = []
        self.enemies = []
        self.boosters = []
        self.particles = []
        self.shockwaves = []
        self.trail = []

        self.score = 0
        self.lives = 3
        self.level = 1

        self.spawn_timer = 0
        self.booster_timer = 0
        self.cooldown = 0
        self.hit_flash = 0
        self.shake = 0
        self.active_boosters = {}
        self.game_over = False

    def _init_starfield(self):
        layers = []
        for count, speed in [(60, 1), (35, 2), (18, 3.5)]:
            layer = []
            for _ in range(count):
                layer.append({
                    "x": random.randint(0, SCREEN_WIDTH),
                    "y": random.randint(0, SCREEN_HEIGHT),
                    "speed": speed,
                    "size": random.choice([1, 1, 2]),
                    "phase": random.uniform(0, 2 * math.pi),
                    "warm": random.random() < 0.25,
                })
            layers.append(layer)
        return layers

    def trigger_explosion(self, x, y, color=(255, 160, 40)):
        for _ in range(16):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, 5.5)
            self.particles.append(
                Particle(
                    x, y,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    random.randint(18, 34),
                    color,
                    random.randint(2, 4),
                    "dot"
                )
            )
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 7)
            self.particles.append(
                Particle(
                    x, y,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    random.randint(10, 18),
                    WHITE,
                    random.randint(4, 8),
                    "spark"
                )
            )
        self.shockwaves.append({"x": x, "y": y, "r": 4, "life": 18, "color": color})

    def render_glow_text(self, text, font, color, glow_color):
        base_surf = font.render(text, True, color)
        glow_surf = font.render(text, True, glow_color)
        out = pygame.Surface((base_surf.get_width() + 8, base_surf.get_height() + 8), pygame.SRCALPHA)

        for offset_x, offset_y in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            temp = glow_surf.copy()
            temp.set_alpha(90)
            out.blit(temp, (4 + offset_x, 4 + offset_y))

        out.blit(base_surf, (4, 4))
        return out

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(1)

        # Player engine trail
        self.trail.append({"x": self.player.x + 22, "y": self.player.y + 46, "life": 14})
        for item in self.trail[:]:
            item["life"] -= 1
            if item["life"] <= 0:
                self.trail.remove(item)

        # Firing system
        if self.cooldown > 0:
            self.cooldown -= 1

        fire_rate = 8 if "rapid" in self.active_boosters else 14
        if keys[pygame.K_SPACE] and self.cooldown <= 0:
            bx = self.player.x + 22 - 3
            by = self.player.y
            if "multi" in self.active_boosters:
                self.bullets.append({"rect": pygame.Rect(bx - 12, by + 6, 6, 16), "vx": -1.5})
                self.bullets.append({"rect": pygame.Rect(bx, by, 6, 16), "vx": 0})
                self.bullets.append({"rect": pygame.Rect(bx + 12, by + 6, 6, 16), "vx": 1.5})
            else:
                self.bullets.append({"rect": pygame.Rect(bx, by, 6, 16), "vx": 0})
            self.cooldown = fire_rate

        for bullet in self.bullets[:]:
            bullet["rect"].y -= 10
            bullet["rect"].x += bullet["vx"]
            if bullet["rect"].y < -20:
                self.bullets.remove(bullet)

        # Difficulty progression
        self.level = 1 + self.score // SCORE_PER_LEVEL
        enemy_speed = 2.6 + (self.level - 1) * 0.5
        spawn_delay = max(10, 26 - (self.level - 1) * 2)

        # Spawning logic
        self.spawn_timer += 1
        if self.spawn_timer > spawn_delay:
            ex = random.randint(0, SCREEN_WIDTH - 30)
            self.enemies.append({
                "rect": pygame.Rect(ex, -30, 30, 30),
                "variant": random.randint(0, 2),
                "phase": random.uniform(0, 2 * math.pi),
            })
            self.spawn_timer = 0

        self.booster_timer += 1
        if self.booster_timer > 380:
            bx = random.randint(0, SCREEN_WIDTH - 26)
            kind = random.choice(["rapid", "shield", "multi", "life"])
            self.boosters.append({"rect": pygame.Rect(bx, -26, 26, 26), "kind": kind})
            self.booster_timer = 0

        # Entity Movement
        for enemy in self.enemies[:]:
            enemy["rect"].y += enemy_speed
            if enemy["rect"].y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)

        for booster in self.boosters[:]:
            booster["rect"].y += 3
            if booster["rect"].y > SCREEN_HEIGHT:
                self.boosters.remove(booster)

        # Powerup durations
        for key in list(self.active_boosters.keys()):
            self.active_boosters[key] -= 1
            if self.active_boosters[key] <= 0:
                del self.active_boosters[key]

        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.shake > 0:
            self.shake -= 1

        # Powerup pickups
        for booster in self.boosters[:]:
            if self.player.rect.colliderect(booster["rect"]):
                kind = booster["kind"]
                if kind == "life":
                    self.lives = min(5, self.lives + 1)
                else:
                    self.active_boosters[kind] = BOOSTER_DURATIONS[kind]
                self.trigger_explosion(booster["rect"].centerx, booster["rect"].centery, BOOSTER_COLORS[kind])
                self.boosters.remove(booster)

        # Enemy collisions
        has_shield = "shield" in self.active_boosters
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy["rect"]):
                self.trigger_explosion(enemy["rect"].centerx, enemy["rect"].centery, (255, 100, 60))
                self.enemies.remove(enemy)
                if not has_shield:
                    self.lives -= 1
                    self.hit_flash = 20
                    self.shake = 16
                    if self.lives <= 0:
                        self.game_over = True
                continue

            for bullet in self.bullets[:]:
                if enemy["rect"].colliderect(bullet["rect"]):
                    self.trigger_explosion(enemy["rect"].centerx, enemy["rect"].centery, (255, 200, 60))
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.score += 10
                    break

        # Visual Effects Updates
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

        for wave in self.shockwaves[:]:
            wave["r"] += 4
            wave["life"] -= 1
            if wave["life"] <= 0:
                self.shockwaves.remove(wave)

        # Background Star Updates
        for layer in self.stars:
            for star in layer:
                star["y"] += star["speed"]
                if star["y"] > SCREEN_HEIGHT:
                    star["y"] = 0
                    star["x"] = random.randint(0, SCREEN_WIDTH)

        for asteroid in self.asteroids:
            asteroid.update()

        # Comet events
        self.comet_timer += 1
        if self.comet_timer > 260 and random.random() < 0.02:
            start_x = random.choice([-20, SCREEN_WIDTH + 20])
            self.comets.append({
                "x": start_x,
                "y": random.randint(0, SCREEN_HEIGHT // 2),
                "angle": math.radians(35 if start_x < 0 else 145),
                "speed": random.uniform(5, 8),
                "life": 90,
                "max_life": 90,
            })
            self.comet_timer = 0

        for comet in self.comets[:]:
            comet["x"] += math.cos(comet["angle"]) * comet["speed"]
            comet["y"] += math.sin(comet["angle"]) * comet["speed"]
            comet["life"] -= 1
            if comet["life"] <= 0 or comet["y"] > SCREEN_HEIGHT + 40:
                self.comets.remove(comet)

    def draw(self, surface, ticks):
        bg_idx = min(len(self.backgrounds) - 1, (self.level - 1) % len(self.backgrounds))
        surface.blit(self.backgrounds[bg_idx], (0, 0))

        # Render Debris / Asteroids
        for asteroid in self.asteroids:
            rotated = pygame.transform.rotate(asteroid.image, asteroid.angle)
            tinted = rotated.copy()
            tinted.fill((160, 170, 190, 255), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(tinted, (asteroid.x - tinted.get_width() / 2, asteroid.y - tinted.get_height() / 2))

        # Render Comets
        for comet in self.comets:
            alpha = max(0, min(255, int(255 * (comet["life"] / comet["max_life"]))))
            tail_len = 70
            end_x = comet["x"] - math.cos(comet["angle"]) * tail_len
            end_y = comet["y"] - math.sin(comet["angle"]) * tail_len
            comet_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(comet_surf, (200, 230, 255, alpha), (comet["x"], comet["y"]), (end_x, end_y), 2)
            pygame.draw.circle(comet_surf, (255, 255, 255, alpha), (int(comet["x"]), int(comet["y"])), 3)
            surface.blit(comet_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Render Stars
        for layer in self.stars:
            for star in layer:
                twinkle = 0.6 + 0.4 * math.sin(ticks * 0.004 + star["phase"])
                val = min(255, int((140 + star["speed"] * 30) * twinkle))
                color = (val, min(255, int(val * 0.85)), 210) if star["warm"] else (val, val, 255)
                pygame.draw.circle(surface, color, (int(star["x"]), int(star["y"])), star["size"])

        if not self.game_over:
            # Engine particles
            for t in self.trail:
                alpha = max(0, int(120 * (t["life"] / 14)))
                trail_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
                pygame.draw.circle(trail_surf, (0, 180, 255, alpha), (5, 5), 4)
                surface.blit(trail_surf, (t["x"] - 5, t["y"] - 5), special_flags=pygame.BLEND_RGBA_ADD)

            # Boosters
            for booster in self.boosters:
                cx, cy = booster["rect"].center
                color = BOOSTER_COLORS[booster["kind"]]
                pulse = 15 + 3 * math.sin(ticks * 0.008 + booster["rect"].x)
                ring = pygame.Surface((int(pulse * 2 + 6), int(pulse * 2 + 6)), pygame.SRCALPHA)
                rcx = ring.get_width() // 2
                pygame.draw.circle(ring, (*color, 90), (rcx, rcx), rcx, 2)
                surface.blit(ring, (cx - ring.get_width() // 2, cy - ring.get_height() // 2), special_flags=pygame.BLEND_RGBA_ADD)
                surface.blit(self.booster_imgs[booster["kind"]], booster["rect"].topleft)

            # Lasers & Enemies
            for bullet in self.bullets:
                img = self.laser_multi_img if bullet["vx"] != 0 else self.laser_img
                surface.blit(img, bullet["rect"].topleft)

            for enemy in self.enemies:
                bob = int(2 * math.sin(ticks * 0.006 + enemy["phase"]))
                surface.blit(self.aliens[enemy["variant"]], (enemy["rect"].x, enemy["rect"].y + bob))

            # Active Shield Effect
            if "shield" in self.active_boosters:
                radius = 30 + int(3 * math.sin(ticks * 0.01))
                shield_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(shield_surf, (0, 200, 255, 60), (radius, radius), radius)
                pygame.draw.circle(shield_surf, (0, 200, 255, 140), (radius, radius), radius, 3)
                surface.blit(shield_surf, (self.player.x + 22 - radius, self.player.y + 22 - radius), special_flags=pygame.BLEND_RGBA_ADD)

            # Ship Thruster Flame
            flicker = 5 + int(4 * abs(math.sin(ticks * 0.03)))
            keys = pygame.key.get_pressed()
            flame_h = flicker + (5 if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] else 0)
            flame_surf = pygame.Surface((26, flame_h + 12), pygame.SRCALPHA)
            flame_col = GOLD if "rapid" in self.active_boosters else (255, 120, 30)

            pygame.draw.polygon(flame_surf, (*flame_col, 180), [(3, 0), (13, flame_h), (23, 0)])
            pygame.draw.polygon(flame_surf, (255, 220, 80, 220), [(8, 0), (13, flame_h - 5), (18, 0)])
            surface.blit(flame_surf, (self.player.x + 9, self.player.y + 44))

            # Player Ship
            surface.blit(self.ship_img, (self.player.x, self.player.y - 3))

            # Screen overlays
            if self.hit_flash > 0:
                flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                flash_surf.fill((255, 0, 0, int(90 * (self.hit_flash / 20))))
                surface.blit(flash_surf, (0, 0))

            surface.blit(self.vignette, (0, 0))

            # HUD
            hud_surf = pygame.Surface((SCREEN_WIDTH, 48), pygame.SRCALPHA)
            hud_surf.fill((10, 10, 25, 150))
            pygame.draw.line(hud_surf, (80, 200, 255, 120), (0, 47), (SCREEN_WIDTH, 47), 2)
            surface.blit(hud_surf, (0, 0))

            score_txt = self.render_glow_text(f"Score: {self.score}", self.font, WHITE, CYAN)
            surface.blit(score_txt, (11, 8))

            lvl_txt = self.render_glow_text(f"Level {self.level}", self.font, GOLD, (255, 150, 0))
            surface.blit(lvl_txt, (SCREEN_WIDTH // 2 - lvl_txt.get_width() // 2, 8))

            for i in range(self.lives):
                lx = SCREEN_WIDTH - 30 - i * 26
                pygame.draw.polygon(surface, RED, [(lx, 18), (lx - 8, 30), (lx, 27), (lx + 8, 30)])

            progress = (self.score % SCORE_PER_LEVEL) / SCORE_PER_LEVEL
            pygame.draw.rect(surface, (20, 20, 35), (0, 47, SCREEN_WIDTH, 3))
            pygame.draw.rect(surface, GOLD, (0, 47, int(SCREEN_WIDTH * progress), 3))

        else:
            # Game Over Screen
            surface.blit(self.vignette, (0, 0))
            over_txt = self.render_glow_text("GAME OVER", self.font_bg, RED, (255, 150, 150))
            final_txt = self.render_glow_text(f"Final Score: {self.score}", self.font, WHITE, CYAN)
            reach_txt = self.render_glow_text(f"Reached Level {self.level}", self.font, GOLD, (255, 150, 0))
            retry_txt = self.font.render("Press 'R' to Restart", True, (180, 180, 180))

            surface.blit(over_txt, (SCREEN_WIDTH // 2 - over_txt.get_width() // 2, SCREEN_HEIGHT // 3 - 20))
            surface.blit(final_txt, (SCREEN_WIDTH // 2 - final_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
            surface.blit(reach_txt, (SCREEN_WIDTH // 2 - reach_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 44))
            surface.blit(retry_txt, (SCREEN_WIDTH // 2 - retry_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 84))

    async def run(self):
        running = True
        scene = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        while running:
            self.clock.tick(FPS)
            ticks = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset()

            self.update()
            self.draw(scene, ticks)

            # Camera Shake Handling
            if self.shake > 0:
                magnitude = int(self.shake * 0.6)
                offset_x = random.randint(-magnitude, magnitude)
                offset_y = random.randint(-magnitude, magnitude)
            else:
                offset_x = offset_y = 0

            self.screen.fill((0, 0, 0))
            self.screen.blit(scene, (offset_x, offset_y))
            pygame.display.flip()

            # REQUIRED for pygbag/browser builds: hand control back to the
            # browser event loop every frame, or the page never repaints
            # and you get a blank/grey canvas.
            await asyncio.sleep(0)

        pygame.quit()


async def main():
    game = SpaceGame()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())