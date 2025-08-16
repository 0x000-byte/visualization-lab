using Plots

# choose a backend (the docs use PythonPlot; comment this out if you prefer GR)
pythonplot(size = (400, 300))  # or: gr(size=(400,300))

# data (from the docs)
n = 100
x = range(0, 1, length = n)
y = randn(n, 3)

# the plotting command (from the docs)
plt = plot(
    x, y,
    line = (0.5, [4 1 0], [:path :scatter :histogram]),
    normalize = true,
    bins = 30,
    marker = (10, 0.5, [:none :+ :none]),
    color = [:steelblue :orangered :green],
    fill = 0.5,
    orientation = [:v :v :h],
    title = "My title",
)

display(plt)  # ensure it shows in REPL/script
savefig("pipeline_example.svg")

