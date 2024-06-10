from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import math

class Vertex:
    def __init__(self, n, directed):
        self.number = n
        self.label = f"Vertex {n}"
        self.radius = 10
        if directed:
            self.color = QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = QtGui.QColor(200, 200, 255)

class Edge:
    def __init__(self, V0, V1, color, directed):
        self.v0 = V0
        self.v1 = V1
        self.color = color if directed else QtGui.QColor(0, 0, 0)

class GraphAsMatrix:
    def __init__(self, n, directed):
        self._isDirected = directed
        self.vertices = [Vertex(i, directed) for i in range(n)]
        self.adjacencyMatrix = [[None for _ in range(n)] for _ in range(n)]
        self.numberOfEdges = 0
        self.edges = []

    @property
    def isDirected(self):
        return self._isDirected

    def isEdge(self, u, v):
        return self.adjacencyMatrix[u][v] is not None

    def addEdge(self, u, v):
        if self.adjacencyMatrix[u][v] is None:
            edge = Edge(self.vertices[u], self.vertices[v], self.vertices[u].color, self.isDirected)
            self.adjacencyMatrix[u][v] = edge
            self.numberOfEdges += 1
            self.edges.append(edge)
            if not self.isDirected:
                self.adjacencyMatrix[v][u] = Edge(self.vertices[v], self.vertices[u], self.vertices[v].color, self.isDirected)

class GraphWidget(QtWidgets.QWidget):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.setMinimumSize(800, 600)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        radius = 10
        margin = 40
        cols = 4
        for i, vertex in enumerate(self.graph.vertices):
            col = i % cols
            row = i // cols
            x = margin + col * 100
            y = margin + row * 100
            qp.setBrush(vertex.color)
            qp.drawEllipse(QtCore.QPointF(x, y), radius, radius)
            qp.drawText(x - radius // 2, y - radius // 2, vertex.label)
            vertex.x, vertex.y = x, y

        for i in range(len(self.graph.vertices)):
            for j in range(len(self.graph.vertices)):
                if self.graph.isEdge(i, j):
                    edge = self.graph.adjacencyMatrix[i][j]
                    x1, y1 = self.graph.vertices[i].x, self.graph.vertices[i].y
                    x2, y2 = self.graph.vertices[j].x, self.graph.vertices[j].y
                    new_x1, new_y1 = self.get_edge_endpoint(x1, y1, x2, y2, radius)
                    new_x2, new_y2 = self.get_edge_endpoint(x2, y2, x1, y1, radius)
                    qp.setPen(QtGui.QPen(edge.color, 2))
                    qp.drawLine(new_x1, new_y1, new_x2, new_y2)
                    if self.graph.isDirected:
                        self.drawArrow(qp, new_x1, new_y1, new_x2, new_y2, edge.color)

    def get_edge_endpoint(self, x1, y1, x2, y2, radius):
        angle = math.atan2(y2 - y1, x2 - x1)
        x = x1 + radius * math.cos(angle)
        y = y1 + radius * math.sin(angle)
        return x, y

    def drawArrow(self, qp, x1, y1, x2, y2, color):
        qp.setPen(QtGui.QPen(color, 2))
        arrow_size = 10
        angle = math.atan2(y2 - y1, x2 - x1)

        #x_arrow = x2 - arrow_size * math.cos(angle)
        #y_arrow = y2 - arrow_size * math.sin(angle)

        left_angle = angle + math.pi / 4
        right_angle = angle - math.pi / 4

        x_left = x2 - arrow_size * math.cos(left_angle)
        y_left = y2 - arrow_size * math.sin(left_angle)

        x_right = x2 - arrow_size * math.cos(right_angle)
        y_right = y2 - arrow_size * math.sin(right_angle)

        qp.drawLine(x2, y2, x_left, y_left)
        qp.drawLine(x2, y2, x_right, y_right)

def main():
    app = QtWidgets.QApplication(sys.argv)

    directed = True  # Change to False for undirected graph
    graph = GraphAsMatrix(20, directed)
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (4, 5), (5, 6), (6, 7), (7, 8),
        (8, 9), (9, 10), (10, 11), (11, 12),
        (12, 13), (13, 14), (14, 15), (15, 16),
        (16, 17), (17, 18), (18, 19), (10, 19), (3, 18), (12, 18), (15, 16),
        (11, 17), (2, 19), (3, 18), (4, 18)
    ]
    for u, v in edges:
        graph.addEdge(u, v)

    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(window)
    graph_widget = GraphWidget(graph)
    layout.addWidget(graph_widget)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
