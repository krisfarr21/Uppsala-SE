# Install the package
install.packages("DeliveryMan_1.2.0.tar.gz", repos = NULL, type="source")


# Load the library
library("DeliveryMan")
myFunction <- function(roads, car, packages){
  nextMove = 0 ###car$nextMove nextmove
  if (car[['load']]==0) {
    pick_up_distance = list()
    for (i in 1: nrow(packages)){
      if (packages[[i, 5]] == 0) {
        distance = abs(car$x - packages[[i, 1]]) + abs(car$y - packages[[i, 2]])
        pick_up_distance = append(pick_up_distance, distance)
      }
      else{pick_up_distance = append(pick_up_distance, 30)}
    }
    idx = which.min(pick_up_distance) #which package to pick up
    goal = packages[cbind(idx, c(1,2))] #first two col of idx row
  }
  else{
    goal = packages[cbind(car[['load']], c(3,4))]
  }

  if ((car$x == goal[[1]]) && (car$y == goal[[2]])) {next_posi <-c(goal[[1]], goal[[2]])}
  else {next_posi <- a_star(roads, car$x, car$y, goal)}
  if (car$x == next_posi[[1]]){
    if (car$y < next_posi[[2]]){nextMove=8}
    else if (car$y > next_posi[[2]]) {nextMove=2}
    else {nextMove=5}
  }
  else if (car$x < next_posi[[1]]){nextMove=6}
  else {nextMove=4}
  car$nextMove=nextMove
  return (car)
}
  

a_star <- function(roads, x, y, goal){ #roads, current postion in this turn, where to go(goal)
  dim <- nrow(roads$hroads)+1
  frontiers <- c()
  expanded <- c()
  while ((x != goal[[1]]) || (y != goal[[2]])) {
    traffic <- list()
    position <- list(c(x+1, y), c(x-1, y), c(x, y-1), c(x,y+1)) #possible moving direction
    for (element in position){
      if ((element[[1]] > 0) && (element[[1]] <= dim)){ # check 
        if ((element[[2]] > 0) && (element[[2]] <= dim)){ # check y
          if (identical(element[[1]], x)){
            if (element[[2]] < y){
              node <- c(element[[1]], element[[2]], roads$vroads[element[[1]], element[[2]]])
              len <- length(traffic)
              traffic[[len+1]] <- node
            }
            else{
              node <- c(element[[1]], element[[2]], roads$vroads[x,y])
              len <- length(traffic)
              traffic[[len+1]] <- node
            }
          }
          else if (identical(element[[2]], y)){
            if (element[[1]] < x){
              node <- c(element[[1]], element[[2]], roads$hroads[element[[1]], element[[2]]])
              len <- length(traffic)
              traffic[[len+1]] <- node
            }
            else{
              node <- c(element[[1]], element[[2]], roads$hroad[x,y])
              len <- length(traffic)
              traffic[[len+1]] <- node
            }
          }
        }
      }
    }
    for (road in traffic){ #traffic stores info about where the car can move
      h <- abs(road[[1]] - goal[[1]]) + abs(road[[2]] - goal[[2]])
      move <- list(road[[1]], road[[2]])
      if (length(expanded) == 0){ #step 0/1
        g <- road[[3]]
        f <- g+h
        first_move <- list(move)
        frontiers <- rbind(frontiers, c(road[[1]], road[[2]], g, h, f, first_move))
      }
      else{
        g <- road[[3]] + expanded[[3]]
        f <- g+h
        first_move <- expanded[6:7]
        add <- TRUE
        for (i in 1:nrow(frontiers)){
          frontier <- frontiers[i,]
          if (identical(frontier[c(1,2)], list(road[[1]], road[[2]]))){
            add <- FALSE
            if (f < frontier[[5]]){
              frontiers[i,] <- c(road[[1]], road[[2]], g, h, f, first_move)
            }
          }
        }
        if (add) {frontiers <- rbind(frontiers, c(road[[1]], road[[2]], g, h, f, first_move))} #the node is not in frontiers
      }
    }
    min_score <- which.min(frontiers[,5])
    expanded <- matrix(frontiers[min_score,], ncol=7)#expanded the node with smallest f
    frontiers <- matrix(frontiers[-min_score,], ncol=7)
    x <- expanded[[1]]
    y <- expanded[[2]]
  }
  return(expanded[[6]])
}  
runDeliveryMan(
  carReady = myFunction,
  dim = 10,
  turns = 2000,
  doPlot = T,
  pause = 0.1,
  del = 5,
  verbose = T
)

testDM(
  myFunction,
  verbose = 0,
  returnVec = FALSE,
  n = 500,
  seed = 21,
  timeLimit = 250
)

