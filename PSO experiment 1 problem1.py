import numpy as np
import matplotlib.pyplot as plt
import xlwt



class PSO(object):
    def __init__(self, population_size, max_steps):
        self.w = 0.6  # 惯性权重
        self.c1 = self.c2 = 2       #学习因子
        self.population_size = population_size  # 粒子群数量
        self.dim = 30  # 搜索空间的维度
        self.max_steps = max_steps  # 迭代次数
        self.x_bound = [-100, 100]  # 解空间范围
        self.x = np.random.uniform(self.x_bound[0], self.x_bound[1],(self.population_size, self.dim))  # 初始化粒子群位置
        self.v = np.random.rand(self.population_size, self.dim)  # 初始化粒子群速度
        fitness = self.calculate_fitness(self.x)
        self.p = self.x  # 个体的最佳位置
        self.pg = self.x[np.argmin(fitness)]  # 全局最佳位置
        self.individual_best_fitness = fitness  # 个体的最优适应度
        self.global_best_fitness = np.min(fitness)  # 全局最佳适应度

    def calculate_fitness(self, x):
        return np.sum(np.square(x), axis=1)

    def evolve(self):
        # fig = plt.figure()
        for step in range(self.max_steps):
            r1 = np.random.rand(self.population_size, self.dim)
            r2 = np.random.rand(self.population_size, self.dim)
            # 更新速度和权重
            self.v = self.w * self.v + self.c1 * r1 * (self.p - self.x) + self.c2 * r2 * (self.pg - self.x)
            self.x = self.v + self.x
            # plt.clf()
            # plt.scatter(self.x[:, 0], self.x[:, 1], s=30, color='k')
            # plt.xlim(self.x_bound[0], self.x_bound[1])
            # plt.ylim(self.x_bound[0], self.x_bound[1])
            # plt.pause(0.01)
            fitness = self.calculate_fitness(self.x)
            # 需要更新的个体
            update_id = np.greater(self.individual_best_fitness, fitness)
            self.p[update_id] = self.x[update_id]
            self.individual_best_fitness[update_id] = fitness[update_id]
            # 新一代出现了更小的fitness，所以更新全局最优fitness和位置
            if np.min(fitness) < self.global_best_fitness:
                self.pg = self.x[np.argmin(fitness)]
                self.global_best_fitness = np.min(fitness)
            # print('%.1f best fitness: %.20f, mean fitness: %.5f' % (step,self.global_best_fitness, np.mean(fitness)))
        return self.global_best_fitness


work_book=xlwt.Workbook(encoding='utf-8')
sheet=work_book.add_sheet('25次迭代最优值')
sheet.write(0,0,'迭代次数')
sheet.write(0,1,'最优值')

optimalValue_list = []
for i in range(25):
    pso = PSO(1000, 1500)
    evolve = pso.evolve()
    optimalValue_list.append(evolve)
    sheet.write(i+1,0,str(i+1))
    sheet.write(i+1,1,evolve)
plt.plot(optimalValue_list)
plt.savefig("D:\demo\demo4\PSO problem 1")

work_book.save('PSO problem1.xls')
# plt.show()