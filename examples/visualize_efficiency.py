import matplotlib.pyplot as plt
from une.une_atomic_library import unified_effective_power, unified_power_acceleration

def plot_efficiency_scaling(max_n=200):
    ns = list(range(1, max_n+1, 5))
    powers = [unified_effective_power(1000, 3600, n) for n in ns]
    accelerations = [unified_power_acceleration(1000, 3600, n, epochs=5) for n in ns]

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(ns, powers)
    plt.title("Effective Power vs Cooperators (N)")
    plt.xlabel("N (cooperators)")
    plt.ylabel("Effective Power (W)")

    plt.subplot(1, 2, 2)
    plt.plot(ns, accelerations)
    plt.title("Power Acceleration vs N")
    plt.xlabel("N")
    plt.ylabel("Acceleration (W/s²)")

    plt.tight_layout()
    plt.savefig("efficiency_scaling.png")
    print("Saved efficiency_scaling.png")

if __name__ == "__main__":
    plot_efficiency_scaling()
