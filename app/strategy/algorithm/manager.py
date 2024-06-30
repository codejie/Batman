"""
Algorithm Manager
"""
from app.strategy.algorithm import Algorithm
from app.strategy.algorithm.check_rate_threshold import CheckRateThresholdAlgorithm
from app.strategy.algorithm.m_up_n_down import MUpNDownAlgorithem

class AlgorithmManager:
  listAlgorithm: dict[str, Algorithm] = {} # name + algorithm

  @staticmethod
  def add(algorithm: Algorithm) -> None:
    AlgorithmManager.listAlgorithm[algorithm.name] = algorithm

  @staticmethod
  def get(name: str) -> Algorithm | None:
    return AlgorithmManager.listAlgorithm.get(name, None)
  
  @staticmethod
  def get_list(names: list[str] | None = None) -> list[Algorithm]:
    if names:
      ret = []
      for item in AlgorithmManager.listAlgorithm.values():
        if item.name in names:
          ret.append(item)
      return ret
    else:
      return AlgorithmManager.listAlgorithm.values()


AlgorithmManager.add(MUpNDownAlgorithem)
AlgorithmManager.add(CheckRateThresholdAlgorithm)