
    // Configuration
    const config = {
        totalLevels: 24,      // Total number of levels 
        levelsPerRow: 5,      // Max levels per row
        unlockedLevels: 10    // Number of levels that are unlocked
      };
  
      // Generate random score for unlocked levels
      function getRandomScore() {
        return Math.floor(Math.random() * 1001); // 0-1000
      }
  
      // Calculate stars based on score
      function calculateStars(score) {
        const maxScore = 1000;
        const maxStars = 5;
        return Math.ceil((score / maxScore) * maxStars);
      }
  
      // Generate all levels
      function generateLevels() {
        const levelContainer = document.getElementById('levelContainer');
        
        // First row: levels 1-4
        const firstRow = document.createElement('div');
        firstRow.className = 'level-row';
        for (let level = 1; level <= 4; level++) {
          const isUnlocked = level <= config.unlockedLevels;
          const levelBox = createLevelBox(level, isUnlocked);
          firstRow.appendChild(levelBox);
        }
        levelContainer.appendChild(firstRow);
        
        // Second row: just level 5
        const secondRow = document.createElement('div');
        secondRow.className = 'level-row';
        const level5 = createLevelBox(5, 5 <= config.unlockedLevels);
        secondRow.appendChild(level5);
        levelContainer.appendChild(secondRow);
        
        // Third row: levels 6-9
        const thirdRow = document.createElement('div');
        thirdRow.className = 'level-row';
        for (let level = 6; level <= 9; level++) {
          const isUnlocked = level <= config.unlockedLevels;
          const levelBox = createLevelBox(level, isUnlocked);
          thirdRow.appendChild(levelBox);
        }
        levelContainer.appendChild(thirdRow);
        
        // Fourth row: just level 10
        const fourthRow = document.createElement('div');
        fourthRow.className = 'level-row';
        const level10 = createLevelBox(10, 10 <= config.unlockedLevels);
        fourthRow.appendChild(level10);
        levelContainer.appendChild(fourthRow);
        
        // Add remaining levels in rows of 4-5 if needed
        if (config.totalLevels > 10) {
          let currentRow = document.createElement('div');
          currentRow.className = 'level-row';
          let levelCount = 0;
          
          for (let level = 11; level <= config.totalLevels; level++) {
            const isUnlocked = level <= config.unlockedLevels;
            const levelBox = createLevelBox(level, isUnlocked);
            currentRow.appendChild(levelBox);
            levelCount++;
            
            // Start a new row after 4-5 levels (alternate)
            if ((levelCount === 4 && (level - 11) % 9 < 4) || levelCount === 5) {
              levelContainer.appendChild(currentRow);
              currentRow = document.createElement('div');
              currentRow.className = 'level-row';
              levelCount = 0;
            }
          }
          
          // Add any remaining levels
          if (levelCount > 0) {
            levelContainer.appendChild(currentRow);
          }
        }
      }
  
      // Create a single level box
      function createLevelBox(levelNumber, isUnlocked) {
        const levelBox = document.createElement('div');
        levelBox.className = isUnlocked ? 'level-box' : 'level-box locked';
        
        // Level icon (lock or check)
        const iconElement = document.createElement('div');
        iconElement.className = 'level-icon';
        if (isUnlocked) {
          iconElement.innerHTML = '<span class="check-icon">✓</span>';
        } else {
          iconElement.innerHTML = '<span class="lock-icon">🔒</span>';
        }
        levelBox.appendChild(iconElement);
        
        // Level number
        const numberElement = document.createElement('div');
        numberElement.className = 'level-number';
        numberElement.textContent = levelNumber;
        levelBox.appendChild(numberElement);
        
        // If unlocked, add score and stars
        if (isUnlocked) {
          const score = getRandomScore();
          const stars = calculateStars(score);
          
          // Score
          const scoreElement = document.createElement('div');
          scoreElement.className = 'level-score';
          scoreElement.textContent = `Score: ${score}`;
          scoreElement.style.color = "#666";
          levelBox.appendChild(scoreElement);
          
          // Stars
          const starsContainer = document.createElement('div');
          starsContainer.className = 'stars-container';
          
          for (let i = 1; i <= 5; i++) {
            const starElement = document.createElement('span');
            starElement.className = i <= stars ? 'star active' : 'star';
            starElement.textContent = '★';
            starsContainer.appendChild(starElement);
          }
          
          levelBox.appendChild(starsContainer);
          
          // Add click event for unlocked levels
          levelBox.addEventListener('click', () => {
            alert(`You selected level ${levelNumber}`);
          });
        }
        
        return levelBox;
      }
  
      // Initialize the level screen when the page loads
      document.addEventListener('DOMContentLoaded', generateLevels);