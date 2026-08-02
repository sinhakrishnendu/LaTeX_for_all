# Verify the three rounded values printed in the teaching article.
measurements <- read.csv("data/simulated_measurements.csv")
measurements$difference_mm <- measurements$method_b_mm - measurements$method_a_mm

reported <- c(
  method_a_mean = mean(measurements$method_a_mm),
  method_b_mean = mean(measurements$method_b_mm),
  mean_difference = mean(measurements$difference_mm)
)

print(round(reported, 2))
stopifnot(identical(unname(round(reported, 2)), c(5.12, 5.19, 0.07)))
