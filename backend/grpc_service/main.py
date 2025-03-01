from backend.grpc_service.adapters.repositories import MemoryCutenessRatingRepository
from backend.grpc_service.adapters.repositories import MemoryDifficultyRatingRepository
from backend.grpc_service.adapters.repositories import MemoryPricedDogTreatRepository
from backend.grpc_service.core.services import DogTreatServerCoreV1
from backend.grpc_service.log import log
from backend.grpc_service.server import serve


def main():
    """
    Main entry point for the gRPC server.
    """
    service = DogTreatServerCoreV1(
        difficulty_rating_repository=MemoryDifficultyRatingRepository(),
        cuteness_rating_repository=MemoryCutenessRatingRepository(),
        priced_dog_treat_repository=MemoryPricedDogTreatRepository(),
    )
    log.info(service)
    serve(service)


if __name__ == "__main__":
    main()
