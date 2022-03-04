from math import sqrt, acos, pi
from .constants import *

class Analyzer:

    def __init__(self, game):
        self.game = game
        self.play_on_cycles = game.get_play_on_cycles()
        self.shoot_status = 0
        self.last_shooter = 'not'
        self.shot_data = []

    def line_intersection(self,line1, line2):
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]
        
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
        div = det(xdiff, ydiff)
        if div == 0:
           raise Exception('lines do not intersect!')
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y
            
    def distance(self, p1: list[float], p2: list[float]) -> float:
        return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def distance_sqrd(self, p1: list[float], p2: list[float]) -> float:
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    def dot(self, v1: list[float], v2: list[float]) -> float:
        result = 0.0
        for m, n in zip(v1,v2):
            result += m*n
        return result

    def is_point_inside_triangle(self, a: list[float], b: list[float], c: list[float], point: list[float]) -> bool:
        v0 = [c[0] - a[0], c[1] - a[1]]
        v1 = [b[0] - a[0], b[1] - a[1]]
        v2 = [point[0] - a[0], point[1] - a[1]]

        # Compute dot products
        dot00 = self.dot(v0, v0)
        dot01 = self.dot(v0, v1)
        dot02 = self.dot(v0, v2)
        dot11 = self.dot(v1, v1)
        dot12 = self.dot(v1, v2)

        # Compute barycentric coordinates
        invDenom = 1.0 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom
        v = (dot00 * dot12 - dot01 * dot02) * invDenom

        # Check if point is in triangle
        return (u >= 0.) and (v >= 0.) and(u + v < 1.)

    def get_players_inside_area(self, cycle: int, a: list[float], b: list[float], c: list[float]) -> int:
        players_inside = 0
        for agent in (self.game.left_team.agents+self.game.right_team.agents):
            if cycle in agent.data:
                agent_pos = [agent.data[cycle]['x'], agent.data[cycle]['y']]
                if self.is_point_inside_triangle(a, b, c, agent_pos):
                    players_inside += 1
        return players_inside

    def update_shot_data(self, x: float, y: float, players_inside: int):        
        distance = self.distance([x,y], R_GOAL_POS)
        p1 = self.distance_sqrd([x,y], R_GOAL_TOP_BAR)
        p2 = self.distance_sqrd([x,y], R_GOAL_BOTTOM_BAR)
        p3 = self.distance_sqrd(R_GOAL_TOP_BAR, R_GOAL_BOTTOM_BAR)
        p12 = sqrt(p1)
        p13 = sqrt(p2)
        angle = acos((p1+p2-p3)/(2*p12*p13))
        self.shot_data.append([x,y,distance,angle,players_inside,0])

    def check_shoot(self, key):
        if key in self.game.ball_pos:
            if(key not in self.play_on_cycles):
                self.shoot_status = 0
                
            elif((self.game.ball_pos[key]['Vx']**2 + self.game.ball_pos[key]['Vy']**2)** 0.5  > self.game.server_param['ball_speed_max'] * self.game.server_param['shot_threshold'] ):
                kickers = self.game.get_kickers(key)
                # Right team registered shot
                if(len(kickers)>0 and kickers[0].team.name == self.game.right_team.name and kickers[0].data[key]['x'] < 0 and self.game.ball_pos[key]['Vx']):
                    ball1 = (self.game.ball_pos[key-1]['x'], self.game.ball_pos[key-1]['y'])
                    ball2 = (self.game.ball_pos[key]['x'], self.game.ball_pos[key]['y'])
                    if ball1[0]-ball2[0]>0:
                        (x_right, y_right) = self.line_intersection((ball1,ball2), ((-53.0,1),(-53.0,0)))
                            
                        if 7.5 < abs(y_right) < 17.5:
                            self.shoot_status       =1
                            self.last_shooter = kickers[0]
                            x = abs(kickers[0].data[key]['x'])
                            y = (-1)*kickers[0].data[key]['y']
                            players_inside = self.get_players_inside_area(key,[kickers[0].data[key]['x'],kickers[0].data[key]['y']],L_GOAL_TOP_BAR,L_GOAL_BOTTOM_BAR)
                            self.update_shot_data(x,y,players_inside)  
                        elif abs(y_right) <= 7.5:
                            self.shoot_status       =1
                            self.last_shooter = kickers[0]
                            x = abs(kickers[0].data[key]['x'])
                            y = (-1)*kickers[0].data[key]['y']
                            players_inside = self.get_players_inside_area(key,[kickers[0].data[key]['x'],kickers[0].data[key]['y']],L_GOAL_TOP_BAR,L_GOAL_BOTTOM_BAR)
                            self.update_shot_data(x,y,players_inside)
                # Left team registered shot
                elif(len(kickers)>0 and kickers[0].team.name == self.game.left_team.name and kickers[0].data[key]['x'] > 0 and self.game.ball_pos[key]['Vx']):
                    ball1= (self.game.ball_pos[key-1]['x'], self.game.ball_pos[key-1]['y'])
                    ball2= (self.game.ball_pos[key]['x'], self.game.ball_pos[key]['y'])
                    if ball2[0]-ball1[0]>0:
                        (x_left, y_left) = self.line_intersection((ball1,ball2), ((53.0,1),(53.0,0)))
    
                        if 7.5 < abs(y_left) < 17.5:
                            self.shoot_status       =1
                            self.last_shooter = kickers[0]
                            x = kickers[0].data[key]['x']
                            y = kickers[0].data[key]['y']
                            players_inside = self.get_players_inside_area(key,[kickers[0].data[key]['x'],kickers[0].data[key]['y']],R_GOAL_TOP_BAR,R_GOAL_BOTTOM_BAR)
                            self.update_shot_data(x,y,players_inside)  
                        elif abs(y_left) <= 7.5:
                            self.shoot_status       =1    
                            self.last_shooter = kickers[0]
                            x = kickers[0].data[key]['x']
                            y = kickers[0].data[key]['y']
                            players_inside = self.get_players_inside_area(key,[kickers[0].data[key]['x'],kickers[0].data[key]['y']],R_GOAL_TOP_BAR,R_GOAL_BOTTOM_BAR)
                            self.update_shot_data(x,y,players_inside)                       

    def check_goal(self, key):
        if(key in self.game.play_modes):
            split_play_mode = self.game.play_modes[key].rsplit('_')
            mode = split_play_mode[0]
            side = split_play_mode[-1]
            if(mode == 'goal'):
                side = split_play_mode[1]
                if(side == 'r'):
                    if(self.last_shooter != 'not' and self.last_shooter.team.name == self.game.right_team.name):
                        self.shot_data[-1][-1] = 1
                elif(side == 'l'):
                    if(self.last_shooter != 'not' and self.last_shooter.team.name == self.game.left_team.name):
                        self.shot_data[-1][-1] = 1

    def analyze(self):        
        for key in range(1,self.play_on_cycles[-1]+1):
            self.check_shoot(key)
            self.check_goal(key)
