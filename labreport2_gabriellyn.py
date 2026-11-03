
import streamlit as st
import random
import matplotlib.pyplot as plt

# =====================================
# 1. PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Genetic Algorithm",
    page_icon="🧬",
    layout="centered"
)


# =====================================
# 2. GENETIC ALGORITHM PARAMETERS
# =====================================

POPULATION_SIZE = 300
CHROMOSOME_LENGTH = 80
TARGET_ONES = 50
MAX_GENERATIONS = 50

MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.8
ELITE_SIZE = 2


# =====================================
# 3. GENERATE AN INDIVIDUAL
# =====================================

def create_individual():

    return [
        random.randint(0, 1)
        for _ in range(CHROMOSOME_LENGTH)
    ]


# =====================================
# 4. CREATE POPULATION
# =====================================

def create_population():

    return [
        create_individual()
        for _ in range(POPULATION_SIZE)
    ]


# =====================================
# 5. FITNESS FUNCTION
# =====================================

def fitness(individual):

    number_of_ones = sum(individual)

    return 80 - abs(number_of_ones - TARGET_ONES)


# =====================================
# 6. SELECTION
# =====================================

def selection(population):

    tournament = random.sample(population, 3)

    winner = max(tournament, key=fitness)

    return winner.copy()


# =====================================
# 7. CROSSOVER
# =====================================

def crossover(parent1, parent2):

    if random.random() < CROSSOVER_RATE:

        point = random.randint(
            1, CHROMOSOME_LENGTH - 1
        )

        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        return child1, child2

    return parent1.copy(), parent2.copy()


# =====================================
# 8. MUTATION
# =====================================

def mutation(individual):

    for i in range(CHROMOSOME_LENGTH):

        if random.random() < MUTATION_RATE:

            individual[i] = 1 - individual[i]

    return individual


# =====================================
# 9. GENETIC ALGORITHM
# =====================================

def genetic_algorithm():

    population = create_population()

    history = []

    for generation in range(MAX_GENERATIONS + 1):

        # Evaluate population
        population.sort(
            key=fitness,
            reverse=True
        )

        best = population[0]

        best_score = fitness(best)

        # Record generation history
        history.append({
            "Generation": generation,
            "Best Fitness": best_score,
            "Number of Ones": sum(best)
        })

        # Stop after 50 generations
        if generation == MAX_GENERATIONS:
            break

        # Elitism: preserve the best individuals
        new_population = [
            individual.copy()
            for individual in population[:ELITE_SIZE]
        ]

        # Generate offspring
        while len(new_population) < POPULATION_SIZE:

            parent1 = selection(population)
            parent2 = selection(population)

            child1, child2 = crossover(
                parent1, parent2
            )

            mutation(child1)
            mutation(child2)

            new_population.append(child1)

            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

    best_individual = max(
        population,
        key=fitness
    )

    return best_individual, history


# =====================================
# 10. STREAMLIT INTERFACE
# =====================================

st.title("🧬 Genetic Algorithm Simulator")

st.write(
    "A Genetic Algorithm application to generate "
    "an optimal 80-bit binary pattern."
)

st.divider()

# Display parameters
st.subheader("Algorithm Parameters")

col1, col2 = st.columns(2)

with col1:

    st.metric("Population Size", POPULATION_SIZE)

    st.metric("Chromosome Length", CHROMOSOME_LENGTH)

    st.metric("Target Number of Ones", TARGET_ONES)

with col2:

    st.metric("Generations", MAX_GENERATIONS)

    st.metric("Mutation Rate", MUTATION_RATE)

    st.metric("Crossover Rate", CROSSOVER_RATE)

st.divider()


# =====================================
# 11. RUN GENETIC ALGORITHM
# =====================================

st.subheader("Run Genetic Algorithm")

if st.button("▶ Run Algorithm", type="primary"):

    with st.spinner("Running Genetic Algorithm..."):

        best, history = genetic_algorithm()

    st.success("Genetic Algorithm completed successfully!")

    # Display best binary pattern
    st.subheader("Best Binary Pattern")

    st.code(
        ''.join(map(str, best))
    )

    # Display final results
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Fitness Score",
        fitness(best)
    )

    col2.metric(
        "Number of Ones",
        sum(best)
    )

    col3.metric(
        "Number of Zeros",
        best.count(0)
    )

    st.divider()


    # =====================================
    # 12. FITNESS IMPROVEMENT GRAPH
    # =====================================

    st.subheader("Fitness Improvement")

    fig, ax = plt.subplots(figsize=(9, 4))

    generations = [
        row["Generation"] for row in history
    ]

    fitness_scores = [
        row["Best Fitness"] for row in history
    ]

    ax.plot(
        generations,
        fitness_scores,
        marker="o"
    )

    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness")
    ax.set_title("Genetic Algorithm Fitness Progress")

    ax.set_xlim(0, MAX_GENERATIONS)
    ax.set_ylim(0, 85)

    ax.grid(True)

    st.pyplot(fig)

    plt.close(fig)

    st.divider()


    # =====================================
    # 13. GENERATION HISTORY TABLE
    # =====================================

    st.subheader("Generation History")

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "The table shows the best fitness score and "
        "number of ones for each generation."
    )

    st.divider()


    # =====================================
    # 14. FINAL RESULT
    # =====================================

    st.subheader("Final Result")

    if fitness(best) == 80:

        st.success(
            "Optimal solution found! "
            "Exactly 50 ones and 30 zeros."
        )

    else:

        st.info(
            "The algorithm completed, but "
            "the optimal solution was not found."
        )

else:

    st.info(
        "Click the Run Algorithm button to start "
        "the Genetic Algorithm."
    )
