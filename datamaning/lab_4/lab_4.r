library(dplyr)
library(ggplot2)
library(class)

# Загрузка данных
games <- read.csv("data/games.csv")

# Первичный анализ
str(games)
colSums(is.na(games))

# Формирование датасета для KNN
data_knn <- games %>%
  select(
    HOME_TEAM_WINS,
    PTS_home,
    FG_PCT_home,
    FT_PCT_home,
    FG3_PCT_home,
    AST_home,
    REB_home
  ) %>%
  na.omit()

# Проверка
colSums(is.na(data_knn))
dim(data_knn)

# Подготовка данных
x <- data_knn %>% select(-HOME_TEAM_WINS)
y <- data_knn$HOME_TEAM_WINS

# Нормализация признаков (min-max)
normalize <- function(x) {
  (x - min(x)) / (max(x) - min(x))
}

x_norm <- as.data.frame(lapply(x, normalize))
summary(x_norm)

# Разделение на обучающую и тестовую выборки
set.seed(123)

train_index <- sample(seq_len(nrow(x_norm)), size = 0.7 * nrow(x_norm))

x_train <- x_norm[train_index, ]
x_test  <- x_norm[-train_index, ]

y_train <- y[train_index]
y_test  <- y[-train_index]

dim(x_train)
dim(x_test)

# Подбор оптимального k
k_values <- 1:25
error_rate <- numeric(length(k_values))

for (k in k_values) {
  pred <- knn(
    train = x_train,
    test = x_test,
    cl = y_train,
    k = k
  )
  error_rate[k] <- mean(pred != y_test)
}

# Оптимальное k
which.min(error_rate)

# График зависимости ошибки от k
plot(
  k_values,
  error_rate,
  type = "b",
  pch = 19,
  xlab = "k",
  ylab = "Доля ошибок",
  main = "Зависимость ошибки классификации от k"
)

# Финальная модель KNN
k_opt <- 21

pred_final <- knn(
  train = x_train,
  test = x_test,
  cl = y_train,
  k = k_opt
)

# Оценка качества
conf_matrix <- table(
  Факт = y_test,
  Прогноз = pred_final
)

conf_matrix

# Процент ошибок
mean(pred_final != y_test) * 100

