library(ggplot2)
library(dplyr)
library(tidyr)
library(GGally)
library(corrplot)
library(car)
library(lmtest)
library(broom)
library(ggpmisc)


train <- read.csv("data/playoff_train.csv")
test <- read.csv("data/playoff_test.csv")


head(train)
head(test)

str(train)
summary(train)


ggplot(train, aes(x = min, y = pts)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  theme_minimal() +
  labs(title = "pts ~ min")

ggplot(train, aes(x = fga, y = pts)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE, color = "red") +
  theme_minimal() +
  labs(title = "pts ~ fga")


ggplot(train, aes(x = fg3m, y = pts)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  theme_minimal() +
  labs(title = "pts ~ fg3m")


ggplot(train, aes(x = ast, y = pts)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  theme_minimal() +
  labs(title = "pts ~ ast")


ggplot(train, aes(x = reb, y = pts)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  theme_minimal() +
  labs(title = "pts ~ reb")


ggplot(train, aes(x = tov, y = pts)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  theme_minimal() +
  labs(title = "pts ~ tov")

model_min <- lm(pts ~ min, data = train)
summary(model_min)


model_fga <- lm(pts ~ fga, data = train)
summary(model_fga)


model_fg3m <- lm(pts ~ fg3m, data = train)
summary(model_fg3m)


model_ast <- lm(pts ~ ast, data = train)
summary(model_ast)


model_reb <- lm(pts ~ reb, data = train)
summary(model_reb)


model_tov <- lm(pts ~ tov, data = train)
summary(model_tov)

ggplot(train, aes(x = min, y = pts)) +
  geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", se = TRUE, color = "blue", fill = "lightblue") +
  theme_minimal() +
  labs(title = "Парная регрессия: pts ~ min",
       x = "Minutes Played",
       y = "Points")


library(ggpmisc)

ggplot(train, aes(x = min, y = pts)) +
  geom_point(alpha = 0.4) +
  stat_smooth(method = "lm", se = TRUE, color = "blue", fill = "lightblue") +
  stat_poly_eq(
    aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~~")),
    formula = y ~ x,
    parse = TRUE,
    size = 5
  ) +
  theme_minimal() +
  labs(title = "Парная регрессия: pts ~ min",
       x = "Minutes",
       y = "Points")


library(ggpmisc)

plot_reg <- function(data, xvar) {
  f <- as.formula(paste("pts ~", xvar))
  
  ggplot(data, aes_string(x = xvar, y = "pts")) +
    geom_point(alpha = 0.4) +
    stat_smooth(method = "lm", se = TRUE, color = "blue", fill = "lightblue") +
    stat_poly_eq(
      aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~~")),
      formula = y ~ x,
      parse = TRUE,
      size = 5
    ) +
    theme_minimal() +
    labs(title = paste("Парная регрессия: pts ~", xvar),
         x = xvar,
         y = "Points")
}

plot_reg(train, "min")
plot_reg(train, "fga")
plot_reg(train, "fg3m")
plot_reg(train, "ast")
plot_reg(train, "reb")
plot_reg(train, "tov")


# Значения для прогноза
new_data <- data.frame(
  min = 2400,
  fga = 1300,
  fg3m = 200,
  ast = 400,
  reb = 500,
  tov = 200
)

# Прогноз по модели min
predict(model_min, newdata = new_data, interval = "confidence")

# Прогноз по модели fga
predict(model_fga, newdata = new_data, interval = "confidence")

# Прогноз по модели fg3m
predict(model_fg3m, newdata = new_data, interval = "confidence")

# Прогноз по модели ast
predict(model_ast, newdata = new_data, interval = "confidence")

# Прогноз по модели reb
predict(model_reb, newdata = new_data, interval = "confidence")

# Прогноз по модели tov
predict(model_tov, newdata = new_data, interval = "confidence")


# Множественная линейная регрессия
multi_model <- lm(pts ~ min + fga + fg3m + ast + reb + tov, data = train)

# Сводка модели
summary(multi_model)


# Выбираем только факторы
factors <- train[, c("min", "fga", "fg3m", "ast", "reb", "tov")]

# Корреляционная матрица
cor_matrix <- cor(factors)
cor_matrix

# Визуализация
library(corrplot)
corrplot(cor_matrix, method = "color", type = "upper", tl.cex = 0.8)


new_data <- data.frame(
  min = 2400,
  fga = 1300,
  fg3m = 200,
  ast = 400,
  reb = 500,
  tov = 200
)

predict(multi_model, newdata = new_data, interval = "confidence")

