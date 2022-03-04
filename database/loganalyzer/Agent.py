from math import degrees,atan

class Agent:
    
    def __init__(self, number, team):
        self.team              = team
        self.number            = number
        self.kick_count        = 0
        self.last_tackle_cycle = 0
        self.tackle_count      = 0
        self.data              = {}
        self.result            = {"all_kick":[],"all_tackle":[],"true_kick":[],"true_tackle":[]}   
        self.moved_distance    = 0 
        self.used_stamina      = 0


    def get_data(self):
        return self.data
       
    def set_data(self,\
        cycle,\
        is_kicked,\
        is_tackled,\
        is_in_tackle_area,\
        is_in_kick_area,\
        is_true_tackle,\
        is_true_kick,\
        x,y,Vx,Vy,\
        body,\
        neck,\
        agent_type,\
        view_quality,\
        view_width,\
        effort,\
        stamina,\
        recovery,\
        stamina_capacity,\
        focus_side,\
        focus_num,\
        turn_count,\
        catch_count,\
        move_counte,\
        dash_count,\
        turn_neck_count,\
        change_view_count,\
        say_count,\
        point_to_count,\
        attention_to_count,\
        point_to_x,\
        point_to_y):
        self.data[cycle] = {\
            'view_quality':view_quality,\
            'view_width':view_width,\
            'is_in_tackle_area':is_in_tackle_area,\
            'is_in_kick_area':is_in_kick_area,\
            'is_true_kick':is_true_kick,\
            'is_true_tackle':is_true_tackle,\
            'effort':effort,\
            'stamina':stamina,\
            'recovery':recovery,\
            'stamina_capacity':stamina_capacity,\
            'focus_side':focus_side,
            'focus_num':focus_num,\
            'turn_count':turn_count,\
            'catch_count':catch_count,\
            'move_counte':move_counte,\
            'dash_count':dash_count,\
            'turn_neck_count':turn_neck_count,\
            'change_view_count':change_view_count,\
            'say_count':say_count,\
            'point_to_count':point_to_count,\
            'attention_to_count':attention_to_count,\
            'point_to_x':point_to_x,\
            'point_to_y':point_to_y,\
            'is_kicked':is_kicked,\
            'is_tackled':is_tackled,\
            'x':x,'y':y,'Vx':Vx,'Vy':Vy,\
            'body':body,\
            'neck':neck,\
            'agent_type':agent_type,\
            'lastkickCycle':self.last_tackle_cycle,\
            'last_tackle_cycle':self.last_tackle_cycle\
            }
    
    def distance(self, agent_pos: tuple, object_pos: tuple) -> float:
        return  ((agent_pos[0] - object_pos[0])*(agent_pos[0] - object_pos[0]) + (agent_pos[1] - object_pos[1])*(agent_pos[1] - object_pos[1]))** 0.5

    def distance_in_cycle(self, cycle: int, object_pos: tuple) -> float:
        return  ((self.data[cycle]['x'] - object_pos[0])*(self.data[cycle]['x'] - object_pos[0]) + (self.data[cycle]['y'] - object_pos[1])*(self.data[cycle]['y'] - object_pos[1]))** 0.5
        
    def is_in_tackle_area(self, game, agent_pos: tuple, ball_pos: tuple, agent_type):
        
        agent_type   = game.agent_types[agent_type]
        kick_radius  = agent_type['player_size']+agent_type['kickable_margin']
        dist        = self.distance(agent_pos, ball_pos)
        if(kick_radius >= dist-1.60):
            return True
        else:
            return False
    
    def is_in_kick_area(self, game, agent_pos: tuple, ball_pos: tuple, agent_type):
        agent_type   = game.agent_types[agent_type]
        kick_radius  = agent_type['player_size']+agent_type['kickable_margin']
        dist        = self.distance(agent_pos, ball_pos)
        if(kick_radius >= dist-0.35):
            return True
        else:
            return False
     
    def parse_data(self,cycle,agent_data, game):

        def degree(ball , body): 

            if(ball[0]-body[0] == 0):
                deg = 90
            else:
                deg = degrees(atan((ball[1]-body[1])/(ball[0]-body[0])))

            if(ball[1]<body[1]):
                if ball[0]> body[0]:
                    return 360+deg
                else:
                    return 360-(180-deg)
            else:
                if ball[0]>body[0]:
                    return deg
                else:
                    return 180 +deg

        agent_type = agent_data[1]
        x = agent_data[3]
        y = agent_data[4]
        Vx = agent_data[5]
        Vy = agent_data[6]
        body = agent_data[7]
        neck = agent_data[8]
        view_quality ='not'
        view_width='not'
        effort='not'
        stamina='not'
        recovery='not'
        stamina_capacity='not'
        focus_side='not'
        focus_num='not'
        dash_count='not'
        turn_count='not'
        catch_count='not'
        move_counte='not'
        turn_neck_count='not'
        change_view_count='not'
        say_count='not'
        point_to_count='not'
        attention_to_count='not'
        point_to_x='not'
        point_to_y= 'not'
        for i in range(len(agent_data)):
            if type(agent_data[i])==list:
                if agent_data[i][0]=='v':
                    view_quality = agent_data[i][1]
                    view_width =agent_data[i][2]
                    
                elif agent_data[i][0]=='s':
                    stamina = agent_data[i][1]
                    effort = agent_data[i][2]
                    recovery = agent_data[i][3]
                    stamina_capacity = agent_data[i][4]
                    
                elif agent_data[i][0] =='f':
                    focus_side= agent_data[i][1]
                    focus_num = agent_data[i][2]
                    
                elif agent_data[i][0] == 'c':
                    kick_count = agent_data[i][1]
                    dash_count = agent_data[i][2]
                    turn_count = agent_data[i][3]
                    catch_count = agent_data[i][4]
                    move_counte = agent_data[i][5]
                    turn_neck_count = agent_data[i][6]
                    change_view_count = agent_data[i][7]
                    say_count = agent_data[i][8]
                    tackle_count = agent_data[i][9]
                    point_to_count = agent_data[i][10]
                    attention_to_count = agent_data[i][11]
                    
            elif (i >8 and i <11) and (type(agent_data[i])!=list):
                if i ==9:
                    point_to_x = agent_data[i]
                elif i ==10:
                    point_to_y = agent_data[i]
                    
        is_kicked = self.is_kicked(kick_count,cycle)
        if is_kicked:
            self.result['all_kick']+=[[x,y]]
        is_tackled = self.is_tackled(tackle_count,cycle)
        if is_tackled:
            self.result['all_tackle']+=[[x,y]]
        is_in_kick_area = self.is_in_kick_area(game,(x,y),(game.ball_pos[cycle]['x'],game.ball_pos[cycle]['y']),agent_type)
        is_in_tackle_area = self.is_in_tackle_area(game,(x,y),(game.ball_pos[cycle]['x'],game.ball_pos[cycle]['y']),agent_type)
        agent_pos = [x,y]
        
        is_true_kick = False
        is_true_tackle = False
        if body<0:
            bodyDegree = 360 +body
        else :
            bodyDegree = body
            
        ball_pos = [game.ball_pos[cycle]['x'],game.ball_pos[cycle]['y']]
        if cycle-1 in self.data:            
            if self.data[cycle-1]['is_in_kick_area']==True and is_kicked== True:
                is_true_kick = True
                self.result["true_kick"]+=[[x,y]]
            else: 
                is_true_kick = False
            if self.data[cycle-1]['is_in_tackle_area']==True and is_tackled ==True:
                is_true_tackle = True
                self.result["true_tackle"]+=[[x,y]]
            else:
                is_true_tackle =False
            
        self.set_data(
            cycle,\
            is_kicked,\
            is_tackled,\
            is_in_tackle_area,\
            is_in_kick_area,\
            is_true_tackle,\
            is_true_kick,\
            x,y,Vx,Vy,\
            body,\
            neck,\
            agent_type,\
            view_quality,\
            view_width,
            effort,\
            stamina,\
            recovery,\
            stamina_capacity,\
            focus_side,\
            focus_num,\
            turn_count,\
            catch_count,\
            move_counte,\
            dash_count,\
            turn_neck_count,\
            change_view_count,\
            say_count,\
            point_to_count,\
            attention_to_count,\
            point_to_x,\
            point_to_y\
            )
        
    def is_kicked(self, kick_count,cycle):
        if(self.kick_count<kick_count):  
            self.kick_count     = kick_count
            self.last_tackle_cycle = cycle
            return True
        return False
 
    def is_tackled(self,tackle_count,cycle):
        if (self.tackle_count<tackle_count):
            self.tackle_count = tackle_count
            self.last_tackle_cycle = cycle
            return True
        return False
    
    def is_owner(self, kickers, cycle) -> bool:
        if(self in kickers):
            return self.data[cycle]['is_in_kick_area'] or self.data[cycle]['is_in_tackle_area']
        else:
            return False

    def is_close_enough(self, cycle) -> bool:
        return self.data[cycle]['is_in_kick_area'] or self.data[cycle]['is_in_tackle_area']
     
