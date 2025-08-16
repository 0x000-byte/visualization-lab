using Plots
gr(size = (400, 300))

# data
n = 100
x = range(0, 1, length = n)
y = randn(n, 3)

# start an empty plot
p = plot(title = "My title")

# 1) line (:path)
plot!(p, x, y[:, 1];
     seriestype = :path,
     line = (0.5, 4),
     color = :steelblue)

# 2) scatter
scatter!(p, x, y[:, 2];
        marker = (10, 0.5, :circle),
        color = :orangered)

# 3) histogram (horizontal via permute)
histogram!(p, y[:, 3];
          bins = 30,
          normalize = true,
          fill = 0.5,
          color = :green,
          permute = (:x, :y))   # <- replaces orientation=:h

display(p)
savefig(p, "pipeline_example_gr.svg")

