-- CreateTable
CREATE TABLE "Post" (
    "id" SERIAL NOT NULL,
    "datetime" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "open" DECIMAL(65,30) NOT NULL,
    "high" DECIMAL(65,30) NOT NULL,
    "low" DECIMAL(65,30) NOT NULL,
    "close" DECIMAL(65,30) NOT NULL,
    "volume" INTEGER NOT NULL,

    CONSTRAINT "Post_pkey" PRIMARY KEY ("id")
);
