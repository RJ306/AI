from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = DiscreteBayesianNetwork([('Disease', 'Fever'), 
                               ('Disease', 'Cough'), 
                               ('Disease', 'Fatigue'), 
                               ('Disease', 'Chills')])

cpd_disease = TabularCPD('Disease', 2, [[0.7], [0.3]])  # P(flu)=0.3, P(cold)=0.7

cpd_fever = TabularCPD('Fever', 2, [
    [0.9, 0.2],  # flu=0.9, cold=0.2
    [0.1, 0.8]],
    evidence=['Disease'], evidence_card=[2])

cpd_cough = TabularCPD('Cough', 2, [
    [0.8, 0.3],
    [0.2, 0.7]],
    evidence=['Disease'], evidence_card=[2])

cpd_fatigue = TabularCPD('Fatigue', 2, [
    [0.6, 0.1],
    [0.4, 0.9]],
    evidence=['Disease'], evidence_card=[2])

cpd_chills = TabularCPD('Chills', 2, [
    [0.7, 0.1],
    [0.3, 0.9]],
    evidence=['Disease'], evidence_card=[2])

model.add_cpds(cpd_disease, cpd_fever, cpd_cough, cpd_fatigue, cpd_chills)

assert model.check_model()

infer = VariableElimination(model)

posterior = infer.query(['Disease'], evidence={'Fever': 1, 'Cough': 1})
print(f"P(Disease|Fever,Cough):\n{posterior}")

posterior_all = infer.query(['Disease'], evidence={'Fever': 1, 'Cough': 1, 'Chills': 1})
print(f"\nP(Disease|Fever,Cough,Chills):\n{posterior_all}")

fatigue_flu = infer.query(['Fatigue'], evidence={'Disease': 1})
print(f"\nP(Fatigue|Disease=flu):\n{fatigue_flu}")
