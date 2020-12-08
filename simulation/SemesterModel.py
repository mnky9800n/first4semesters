from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import numpy as np

def compute_semester_gpa(model):
    """
    Computes the average gpa for all students
    """
#     pass
    
    return np.mean([a.grade for a in model.schedule.agents])

# def compute_student_gpa():
#     """
#     Computes the average gpa for a single student
#     """
#     pass

class StudentAgent(Agent):
    """
    A student agent who is studying at the university
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        hs_gpa = np.random.normal(2.5, 1)
        self.hs_gpa = 4 if hs_gpa > 4 else hs_gpa
        self.parent_college_educated = np.random.binomial(1, 0.5)
        self.grade = 0
        
    def does_class_work(self):
        prob_does_class_work = 0.25
        
        if self.hs_gpa > 3.0:
            prob_does_class_work += 0.25
        
        if self.parent_college_educated == 1:
            prob_does_class_work += 0.25
            
        return np.random.binomial(1, prob_does_class_work)
    
    def step(self):
        prob_does_cw = self.does_class_work()
        if prob_does_cw > 0.5:
#             print(prob_does_cw)
            self.grade += 1

    
class SemesterModel(Model):
    """
    A model of a semester over 90 days
    """
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.running = True
        
        for i in np.arange(self.num_agents):
            a = StudentAgent(i, self)
            self.schedule.add(a)
            
        self.datacollector = DataCollector(
            model_reporters={'semester_gpa':compute_semester_gpa}
            ,agent_reporters={'student_gpa': 'grade'}
        )
        
    def step(self):
        """
        Advance the model by one step
        """
        self.datacollector.collect(self)
        self.schedule.step()