import matplotlib.pyplot as plt
import numpy as np
import math

# 코사인 유사도에 대한 함수
def reciprocal_score(cosine_similarity):
    if cosine_similarity <= 0.4:
        return 0
    elif cosine_similarity >= 0.8:
        return 1
    else:
        return 1 - np.sqrt(1 - ((cosine_similarity - 0.4) / 0.4) ** 2)

# 코사인 유사도 값 생성
cosine_values = np.linspace(0, 1, 100)
scores = [reciprocal_score(cosine) for cosine in cosine_values]

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(cosine_values, scores, label='Score', color='blue')
plt.title('Cosine Similarity Score vs. Cosine Similarity')
plt.xlabel('Cosine Similarity')
plt.ylabel('Score')
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
plt.axvline(x=0.4, color='red', linestyle='--', linewidth=0.5, label='Threshold (0.4)')
plt.axvline(x=0.8, color='red', linestyle='--', linewidth=0.5, label='Threshold (0.8)')
plt.legend()
plt.grid(True)
plt.show()