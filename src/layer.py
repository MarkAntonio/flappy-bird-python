from enum import IntEnum, auto


class Layer(IntEnum):
    BACKGROUND = auto()
    OBSTACLE = auto()
    FLOOR = auto()
    PLAYER = auto()
    UI = auto()


"""
A função auto() é uma característica interessante das enumerations no Python que atribui automaticamente valores inteiros crescentes às constantes, começando por 1. Isso significa que cada constante terá um valor inteiro único atribuído a ela, incremental em relação ao anterior. Isso é útil quando você quer enumerações com valores distintos sem precisar atribuí-los manualmente.
No seu código, você definiu a enumeração Layer, que parece representar diferentes camadas em um ambiente de jogo (por exemplo, um jogo 2D). Cada constante nessa enumeração representa um tipo de camada:

BACKGROUND: Camada do plano de fundo.
OBSTACLE: Camada de obstáculos.
FLOOR: Camada do chão.
PLAYER: Camada do jogador.
UI: Camada da interface do usuário.
Essas constantes podem ser usadas para representar e distinguir entre os diferentes tipos de camadas em um jogo, por exemplo, ao definir a renderização ou o comportamento de cada camada.

Uma enumeração é útil quando se quer representar um conjunto fixo de valores que não devem ser modificados durante a execução do programa. O IntEnum em particular é útil quando se deseja tratar os valores como inteiros, o que pode ser útil em várias situações, como em comparações numéricas ou cálculos."""