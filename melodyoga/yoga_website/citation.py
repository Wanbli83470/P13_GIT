import time
from datetime import datetime, date, time
today = datetime.now()
today = today.date()
test = datetime(2019, 3, 21, 0, 0)

week = today.isocalendar()

#print(week)

week = week[1]
#print("On veut récupérer le numéro de semaine : {}".format(week))

phrase = ["Celui qui est le maître de lui-même est plus grand que celui qui est le maître du monde.",
          "Doutez de tout et surtout de ce que je vais vous dire.",
          "Il n’existe rien de constant si ce n’est le changement",
          "Le monde est aveugle. Rares sont ceux qui voient correctement.",
          "Le paysan laboure les champs, l’armurier façonne la flèche, le charpentier courbe le bois, mais le sage se perfectionne lui-même.",
          " Le plus grand gain est de donner aux autres. La plus grande perte est de recevoir sans gratitude.",
          "L’insensé reconnaissant sa folie est, en vérité, sage. Mais l’insensé qui se croit sage est vraiment fou.",
          "Mettez-vous à la place des autres. Si vous y arrivez, vous ne serez plus capable de faire du mal à autrui.",
          "On peut allumer des dizaines de bougies à partir d’une seule sans en abréger la vie. On ne diminue pas le bonheur en le partageant.",
          "Quel que soit le nombre de saintes paroles que vous lisez, que vous prononcez, quel bien vous feront-elles si vos actes ne s’y conforment pas ? – citations de bouddha",
          "Rester en colère, c’est comme saisir un charbon ardent avec l’intention de le jeter sur quelqu’un; c’est vous qui vous brûlez.",
          "La paix vient de l’intérieur. Ne la cherchez pas à l’extérieur. – citations de bouddha",
          "Toi seul es ton propre maître. C’est de toi que l’effort doit venir.",
          "Dans toutes les directions, l’homme sage répand le parfum de sa vertu. – citations de bouddha",
          "Personne ne peut nous sauver, à part nous-mêmes… Personne ne peut et personne ne le fera pour nous… Nous devons nous-mêmes marcher dans notre propre voie.",
          "Le don de vérité est un don qui surpasse tous les autres.",
          "Ni dans l’air, ni au milieu de l’océan, ni dans les profondeurs, des montagnes, ni en aucune partie, de ce vaste monde, il n’existe de lieu, où l’être humain, puisse échapper, aux conséquences de ses actes.",
          "La douceur triomphe sur la colère, la générosité triomphe sur la méchanceté, la vérité triomphe sur la tromperie.",
          " Attache-toi au sage qui réprouve tes fautes. – citations de bouddha",
          "Ne suivez pas mon enseignement aveuglément, éprouvez-le par vous-même.",
          "Tout bonheur en ce monde vient de l’ouverture aux autres; toute souffrance vient de l’enfermement en soi-même.",
          "Sachant que la vie est courte, comment pouvez-vous vous quereller ?",
          "Ceux qui refusent d’aspirer à la vérité n’ont pas compris le sens de la vie.",
          "C’est une perle rare en ce monde que d’avoir un cœur sans désir.",
          "Considère celui qui te fait voir tes défauts comme s’il te montrait un trésor.",
          "De celui qui dans la bataille a vaincu mille milliers d’hommes et de celui qui s’est vaincu lui-même, c’est ce dernier qui est le plus grand vainqueur.",
          "Faciles à voir sont les fautes d’autrui. Difficiles à voir sont les nôtres.",
          "La vigilance est le chemin du royaume immortel. La négligence celui qui conduit à la mort.",
          "Le temps est un grand maître, le malheur, c’est qu’il tue ses élèves.",
          "L’esprit est difficile à maîtriser et instable. Il court où il veut. Il est bon de le dominer. L’esprit dompté assure le bonheur.",
          "Ne demeure pas dans le passé, ne rêve pas du futur, concentre ton esprit sur le moment présent.",
          "Si vous voulez connaître votre passé, observez les conditions de votre vie présente, et si vous voulez savoir comment vous vivrez dans l’avenir, regardez ce que vous faites dans le présent.",
          "Si le problème a une solution il ne sert à rien de s’inquiéter, mais s’il n’y a pas de solution, s’inquiéter ne changera rien.",
          "Toute conquête engendre la haine, car le vaincu demeure dans la misère. Celui qui se tient paisible, ayant abandonné toute idée de victoire ou de défaite, se maintient heureux.",
          "Un sot a beau demeurer des années en contact avec la science, il ne connaîtra pas plus le goût de la science que la cuillère plongée dans la sauce ne connaît le goût de la sauce.",
          "Les mots ont le pouvoir de détruire ou de soigner; lorsqu’ils sont justes et généreux, ils peuvent changer le monde.",
          "Votre pire ennemi ne peut pas vous blesser autant que vos pensées. Mais une fois maîtrisées, personne ne vous aidera autant que vos pensées.",
          "La douleur est inévitable, mais la souffrance est facultative.",
          "Vis comme si l’instant le plus important de ta vie était le moment que tu vis maintenant.",
          "Chaque matin, nous renaissons à nouveau. Ce que nous faisons aujourd’hui est ce qui importe le plus.",
          "Un ami qui n’est pas sincère et qui est méchant est plus à craindre qu’une bête sauvage. Une bête sauvage peut blesser votre corps, mais un mauvais ami blessera votre esprit.",
          "Ne t’attache pas à ce que tu possèdes aujourd’hui, car tu peux très bien le perdre demain.",
          "Le doute divise les hommes. C’est un poison qui désagrège les amitiés et détruit les bonnes relations. C’est une épine qui irrite et fait mal; c’est une épée qui tue.",
          "Si tu ne trouves pas d’ami sage, prêt à cheminer avec toi, résolu, constant, marche seul, comme un roi après une conquête, ou un éléphant dans la forêt.",
          "Ne crois que ce que tu juges toi-même être vrai après avoir été éprouvé à la flamme de ton expérience. Sois toi-même ton propre flambeau.",
          "La chute n’est pas un échec. L’échec c’est de rester là où on est tombé.",
          "Un trésor de belles maximes est préférable à un amas de richesses.",
          "Ce qu’on doit chercher à savoir, c’est de quelle façon on doit vivre sa vie pour qu’elle soit la meilleure possible.",
          "Accepte ce qui est, laisse aller ce qui était et aie confiance en ce qui sera.",
          "Le changement n’est jamais douloureux. Seule la résistance au changement est douloureuse.",
          "Ce que tu penses, tu le deviens. Ce que tu ressens, tu l’attires. Ce que tu imagines, tu le crées.",
          "Quelles qu’aient été les difficultés du passé, tu peux toujours recommencer à zéro aujourd’hui.",
          ]

phrase_du_jour = (phrase[week])
#print(phrase[week])