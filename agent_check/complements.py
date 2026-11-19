# The two-by-two table of the advisor note (Table 1 of theory/agent_teams/agent_coordination_note.tex):
# expected passes with B=100 tokens for 100 tasks and no learning phase, depending on whether the team
# observes the difficulty of each task and whether it knows the evaluator's standard.
# A team that does not observe difficulty cannot tell the tasks apart, so it gives every task the same tokens.
from agent_model import model

thL, thH, pi0 = 0.5, 8.0, 0.5
de, dh, ne, nh, B = 0.25, 4.0, 50, 50, 100.0
M = model(thL=thL, thH=thH, pi0=pi0, ne=ne, nh=nh, de=de, dh=dh)
G = lambda pi: M['solve'](pi, B, ne, nh)[0]

def uniform(theta):
    b = B / (ne + nh)
    return ne * b / (b + theta * de) + nh * b / (b + theta * dh)

blind = pi0 * uniform(thH) + (1 - pi0) * uniform(thL)   # same allocation whether or not the standard is known
print("                          standard not known   standard known")
print("difficulty not observed        %.1f                 %.1f" % (blind, blind))
print("difficulty observed            %.1f                 %.1f" % (G(pi0), pi0 * G(1.0) + (1 - pi0) * G(0.0)))
