# Imports
import pygame
import math
pygame.init()
# Config
WIDTH, HEIGHT = pygame.SCALED, pygame.SCALED
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicsans", 16)
pygame.display.set_caption("Planet Simulation")
# Color (RGB)
WHITE = (255, 255, 255)
YELLOW = (255, 200, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
GREEN = (140,255,140)
BROWN = (153,77,0)
LIGHTBROWN = (255,217,179)
LIGHTBLUE = (102,255,255)
DARKBLUE = (13,0,77)
# Functions
def Calculate_Orbital_Radius(A, P):
    return 1/2 * (A + P)
def Calculate_Orbital_Velocity(G, CentralBodyMass, A, P):
    return math.sqrt(G * CentralBodyMass / Calculate_Orbital_Radius(A, P))
def ConvertTime(Time):
    Unit = "Seconds"
    if Time >= 60: # Minute
        Time /= 60
        Unit = "Minute"
        if Time >= 60: # Hour
            Time /= 60
            Unit = "Hour"
            if Time >= 24: # Day
                Time /= 24
                Unit = "Day"
                if Time >= 30: # Month
                    Time /= 30
                    Unit = "Month"
                    if Time >= 12: # Year
                        Time /= 12
                        Unit = "Year"
    return round(Time), Unit
# Classes
class Planet:

	AU = 146*10**9
	G = 6.67428e-11
	GameScale = 1 / AU
	TIMESTEP = 86400
    
	def __init__(self, x, y, radius, color, mass):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win):
		x = self.x * Planet.GameScale + WIDTH / 2
		y = self.y * Planet.GameScale + HEIGHT / 2

		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * Planet.GameScale + WIDTH / 2
				y = y * Planet.GameScale + HEIGHT / 2
				updated_points.append((x, y))

			pygame.draw.lines(win, self.color, False, updated_points, 2)

		pygame.draw.circle(win, self.color, (x, y), (self.radius / Planet.AU) * (Planet.GameScale))
		
		if not self.sun:
			distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.sun:
			self.distance_to_sun = distance

		force = Planet.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * Planet.TIMESTEP
		self.y_vel += total_fy / self.mass * Planet.TIMESTEP

		self.x += self.x_vel * Planet.TIMESTEP
		self.y += self.y_vel * Planet.TIMESTEP
		self.orbit.append((self.x, self.y))
# Main
def main():
	run = True
	clock = pygame.time.Clock()

	sun = Planet(0, 0, 695660, YELLOW, 1.9885 * 10**30)
	sun.sun = True

	mercury = Planet(0.3877060531148948 * Planet.AU, 0, 2440, DARK_GREY, 3.29 * 10**23)
	mercury.y_vel = Calculate_Orbital_Velocity(Planet.G, sun.mass, 0.3877060531148948 * Planet.AU, 0.3877060531148948 * Planet.AU)

	venus = Planet(0.7184393701832681 * Planet.AU, 0, 6052, WHITE, 4.868 * 10**24)
	venus.y_vel = Calculate_Orbital_Velocity(Planet.G, sun.mass, 0.7184393701832681 * Planet.AU, 0.7184393701832681 * Planet.AU)

	earth = Planet(1 * Planet.AU, 0, 6378, BLUE, 5.9736 * 10**24)
	earth.y_vel = Calculate_Orbital_Velocity(Planet.G, sun.mass, 1 * Planet.AU, 1 * Planet.AU)

	mars = Planet(1.524 * Planet.AU, 0, 3390, RED, 6.4169 * 10**23)
	mars.y_vel = Calculate_Orbital_Velocity(Planet.G, sun.mass, 1.524  * Planet.AU, 1.524  * Planet.AU)

	jupiter = Planet(5.204266587511253 * Planet.AU, 0, 69911, BROWN, 1.9 * 10**27)
	jupiter.y_vel = Calculate_Orbital_Velocity(Planet.G, sun.mass, 5.204266587511253 * Planet.AU, 5.204266587511253 * Planet.AU)

	saturn = Planet(9.582017199702284 * Planet.AU, 0, 58232, LIGHTBROWN, 5.68 * 10**26)
	saturn.y_vel = Calculate_Orbital_Velocity(Planet.G, sun.mass, 9.582017199702284 * Planet.AU, 9.582017199702284 * Planet.AU)

	uranus = Planet(19.191263797665282 * Planet.AU, 0, 25362, LIGHTBLUE, 8.68 * 10**25)
	uranus.y_vel = Calculate_Orbital_Velocity(Planet.G, sun.mass, 19.191263797665282 * Planet.AU, 19.191263797665282 * Planet.AU)

	neptune = Planet(30.103661503993145 * Planet.AU, 0, 24764, DARKBLUE, 1.02*10**26)
	neptune.y_vel = Calculate_Orbital_Velocity(Planet.G, sun.mass, 30.103661503993145 * Planet.AU, 30.103661503993145 * Planet.AU)

	planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

	scroll = 1
	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		Fps = round(clock.get_fps())
		FpsText = ""
		if Fps >= 50:
			FpsText = FONT.render(f"{Fps} FPS", 1, GREEN)
		elif Fps >= 30 and Fps < 50:
			FpsText = FONT.render(f"{Fps} FPS", 1, YELLOW)
		elif Fps < 30:
			FpsText = FONT.render(f"{Fps} FPS", 1, RED)
		WIN.blit(FpsText, (0,0))
		
		Time = ConvertTime(Planet.TIMESTEP)
		TimeText = FONT.render(f"{Time[0]} {Time[1]}(s) Passes Every Second", 1, WHITE)
		WIN.blit(TimeText, (0,FpsText.get_height()))

		Planet.GameScale = scroll / Planet.AU

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					scroll *= 1.1
				elif event.button == 5:
					scroll /= 1.1

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()
main()