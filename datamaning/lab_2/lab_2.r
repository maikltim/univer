library(tidyverse)   
library(cluster)     
library(factoextra)  
library(dendextend) 
library(ggrepel)   
library(tidyr)
library(ggplot2)
library(corrplot)
library(dplyr)


data <- read_csv("data/2023_nba_player_stats.csv")
data

var <- c("Min","PTS","REB","AST","STL","BLK","FG%","3P%","FT%","TOV","OREB","DREB","3PM","3PA","FTM","FTA")
data_clust <- data %>% select(any_of(var)) %>% drop_na()

dim(data_clust)

summary(data_clust)


data_clust %>%
  gather(key = "variable", value = "value") %>%
  ggplot(aes(x = value)) +
  geom_histogram(bins = 30, fill = "skyblue", color = "black") +
  facet_wrap(~variable, scales = "free") +
  theme_minimal() +
  ggtitle("Гистограммы распределений числовых переменных")


cor_matrix <- cor(data_clust)
corrplot::corrplot(cor_matrix, method = "color", type = "upper", tl.cex = 0.7)


# центрирование и нормализация (z-score)
data_scaled <- scale(data_clust)  

# считаем Евклидово расстояние между игроками
dist_mat <- dist(data_scaled, method = "euclidean")

# Запускаем иерархическую кластеризацию методом ward.D2
hc_ward <- hclust(dist_mat, method = "ward.D2")

# Визуализация дендрограммы
plot(hc_ward, labels = FALSE, hang = -1, main = "Дендрограмма (Ward.D2)")

# разрез на 4 кластера
rect.hclust(hc_ward, k = 4, border = 2:5) 

# Определение числа кластеров для k-means («локоть»)
wss <- map_dbl(1:10, function(k){
  set.seed(123)
  km <- kmeans(data_scaled, centers = k, nstart = 25)
  km$tot.withinss
})

plot(1:10, wss, type='b', xlab='k (число кластеров)', ylab='SSE', main='График локтя')
abline(v=3, lty=2)  # пример: вертикальная линия на k=3

# K-means кластеризация
k <- 3
set.seed(123)
km_res <- kmeans(data_scaled, centers = k, nstart = 50)
# количество игроков в каждом кластере
table(km_res$cluster)  

D <- as.matrix(dist_mat)
mds2 <- cmdscale(D, k = 2, eig = TRUE)
mds_df <- data.frame(MDS1 = mds2$points[,1], MDS2 = mds2$points[,2], cluster = factor(km_res$cluster), player = data$PName[1:nrow(data_scaled)])

ggplot(mds_df, aes(x = MDS1, y = MDS2, color = cluster)) +
  geom_point(size = 3) +
  geom_text_repel(aes(label = ifelse(seq_len(nrow(mds_df)) %% 10 == 0, player, "")), size = 3) +
  theme_minimal() +
  ggtitle(paste("MDS (cmdscale) — kmeans, k =", k))


clust_table <- data_clust %>%
  as_tibble() %>%
  mutate(cluster = factor(km_res$cluster), player = data$PName[1:nrow(data_scaled)])


cluster_means <- clust_table %>%
  group_by(cluster) %>%
  summarise(across(where(is.numeric), mean, .names = "mean_{col}"))

print(cluster_means)

clust_table %>%
  group_by(cluster) %>%
  slice_head(n = 5) %>%
  select(player, cluster, PTS, REB, AST, `FG%`, `3P%`, `FT%`)


