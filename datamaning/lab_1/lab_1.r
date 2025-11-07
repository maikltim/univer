# ==============================
# 1. Подключение библиотек
# ==============================
library(readr)
library(psych)
library(ggplot2)
library(reshape2)
library(GGally)
library(interactions)

# ==============================
# 2. Загрузка данных
# ==============================
data <- read.csv("Задания/14 Городской транспорт Сан-Пауло/Behavior of the urban traffic of the city of Sao Paulo in Brazil.csv",
                 header = TRUE, sep = ";", stringsAsFactors = FALSE)

dim(data)
head(data)
str(data)

# ==============================
#  3. Предварительная обработка
# ==============================

# Преобразуем целевую переменную в числовой тип
data$Slowness.in.traffic.... <- as.numeric(gsub(",", ".", data$Slowness.in.traffic....))

# Проверим структуру
str(data$Slowness.in.traffic....)

# ==============================
#  4. Описательная статистика
# ==============================
summary(data)
describe(data)

# ==============================
#   5. Анализ выбросов
# ==============================

# Построение boxplot
ggplot(data, aes(y = Slowness.in.traffic....)) +
  geom_boxplot(fill = "#69b3a2", color = "darkblue", outlier.colour = "red") +
  labs(
    title = "Распределение замедленности движения в Сан-Паулу",
    y = "Slowness in traffic (%)"
  ) +
  theme_minimal()

# --- Расчёт квартилей и IQR ---
Q1 <- quantile(data$Slowness.in.traffic...., 0.25)
Q3 <- quantile(data$Slowness.in.traffic...., 0.75)
IQR <- Q3 - Q1

# --- Границы выбросов ---
lower <- Q1 - 1.5 * IQR
upper <- Q3 + 1.5 * IQR

# --- Поиск выбросов ---
outliers <- data$Slowness.in.traffic....[data$Slowness.in.traffic.... < lower |
                                           data$Slowness.in.traffic.... > upper]
outliers
length(outliers)

# --- Создание очищенного набора ---
data_clean <- subset(data, Slowness.in.traffic.... >= lower & Slowness.in.traffic.... <= upper)

nrow(data)
nrow(data_clean)

# ==============================
#  6. Анализ распределений и корреляций
# ==============================

# Выбор числовых переменных
num_vars <- sapply(data_clean, is.numeric)
num_data <- data_clean[, num_vars]

# Статистики
sapply(num_data, median)
sapply(num_data, mean)
sapply(num_data, var)
sapply(num_data, sd)

# --- Корреляционная матрица ---
corr_matrix <- cor(num_data, use = "pairwise.complete.obs")
round(corr_matrix, 2)

# --- Тепловая карта корреляций ---
cor_data <- melt(corr_matrix)

ggplot(cor_data, aes(Var1, Var2, fill = value)) +
  geom_tile(color = "white") +
  scale_fill_gradient2(
    low = "darkred", mid = "white", high = "darkblue",
    midpoint = 0, limit = c(-1, 1), name = "Корреляция"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1)) +
  ggtitle("Тепловая карта корреляций между показателями городского трафика")

# ==============================
# 7. Исследование взаимодействия между предикторами
# ==============================

# Парные зависимости
ggpairs(data_clean[, c("Hour..Coded.",
                       "Immobilized.bus",
                       "Broken.Truck",
                       "Accident.victim",
                       "Semaphore.off",
                       "Slowness.in.traffic....")])

# --- Модель взаимодействий ---
model_inter <- lm(Slowness.in.traffic.... ~ 
                    Hour..Coded. * Accident.victim +
                    Broken.Truck * Semaphore.off +
                    Immobilized.bus * Lack.of.electricity,
                  data = data_clean)

summary(model_inter)

# --- Визуализация взаимодействия ---
interact_plot(model_inter, pred = Hour..Coded., modx = Accident.victim,
              plot.points = TRUE, interval = TRUE,
              x.label = "Hour (Coded)",
              y.label = "Slowness in Traffic (%)",
              main.title = "Взаимодействие между временем и количеством ДТП")


