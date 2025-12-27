library(dplyr)
library(ggplot2)
library(lubridate)


games <- read.csv("data/games.csv")
head(games)

# Преобразование даты
games$GAMES_DATE_EST <- as.Date(games$GAME_DATE_EST)


# Выделяем сезон
games$season <- year(games$GAME_DATE_EST)
games$season[month(games$GAME_DATE_EST) < 7] <- games$season[month(games$GAME_DATE_EST) < 7] - 1

# Фильтр по команде Los Angeles Lakers
lakers_games <- games %>%
  filter(HOME_TEAM_ID == 1610612747 | VISITOR_TEAM_ID == 1610612747) %>%
  mutate(
    points = ifelse(HOME_TEAM_ID == 1610612747, PTS_home, PTS_away)
  )

# Агрегация: средние очки за сезон
season_data <- lakers_games %>%
  group_by(season) %>%
  summarise(avg_points = mean(points)) %>%
  arrange(season)


ggplot(season_data, aes(x = season, y = avg_points)) +
  geom_line(color = "blue") +
  geom_point() +
  labs(
    title = "Среднее количество очков Lakers по сезонам",
    x = "Сезон",
    y = "Очки за матч"
  ) + 
  theme_minimal()
  

# Добавляем временной индекс

season_data$t <- 1:nrow(season_data)
  
# Линейная регрессия
model <- lm(avg_points ~ t, data = season_data)

summary(model)






