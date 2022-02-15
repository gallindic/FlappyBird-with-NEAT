from FlappyBird.flappy_bird import FlappyBird
import neat
import os

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    flappy_bird = FlappyBird()

    winner = population.run(flappy_bird.run, 1000)
    print('\nBest genome:\n{!s}'.format(winner))

    flappy_bird.quit()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    run(config_path)
    