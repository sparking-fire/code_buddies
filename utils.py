import json
from typing import Dict, List, Optional, Tuple
import pandas as pd
import plotly.express as px
from datetime import datetime

class QuestionGenerator:
    """Handles question generation and difficulty management."""
    
    def __init__(self):
        self.difficulty_weights = {
            'beginner': {
                'concept_recall': 0.7,
                'application': 0.2,
                'analysis': 0.1
            },
            'intermediate': {
                'concept_recall': 0.3,
                'application': 0.5,
                'analysis': 0.2
            },
            'advanced': {
                'concept_recall': 0.1,
                'application': 0.4,
                'analysis': 0.5
            }
        }
    
    def generate_prompt(self, content: str, level: str) -> str:
        """Generate appropriate prompt based on difficulty level."""
        weights = self.difficulty_weights[level]
        
        prompt_template = f"""Based on this content, generate a {level} level question.
        Content: {{content}}
        
        Question requirements:
        - {weights['concept_recall']*100}% chance of concept recall
        - {weights['application']*100}% chance of practical application
        - {weights['analysis']*100}% chance of analysis/synthesis
        
        The question should:
        - Be clear and specific
        - Include 4 multiple choice options
        - Have one correct answer
        - Include a detailed explanation
        
        Return as JSON with these keys:
        - question
        - options (array of 4 choices)
        - correct_answer
        - explanation
        - difficulty_level
        """
        
        return prompt_template.format(content=content[:4000])  # Limit content length

class PerformanceAnalyzer:
    """Analyzes student performance and adjusts difficulty."""
    
    def __init__(self):
        self.minimum_questions = 3  # Minimum questions before level change
        self.accuracy_thresholds = {
            'upgrade': 0.75,  # 75% accuracy to move up
            'downgrade': 0.4   # Below 40% accuracy to move down
        }
    
    def calculate_metrics(self, history: List[Dict]) -> Dict:
        """Calculate performance metrics from history."""
        if not history:
            return {
                'accuracy': 0,
                'streak': 0,
                'total_questions': 0,
                'level_appropriate': True
            }
        
        recent = history[-min(len(history), 5):]  # Last 5 questions
        correct = sum(1 for x in recent if x['correct'])
        
        return {
            'accuracy': correct / len(recent),
            'streak': self._calculate_streak(history),
            'total_questions': len(history),
            'level_appropriate': self._is_level_appropriate(recent)
        }
    
    def _calculate_streak(self, history: List[Dict]) -> int:
        """Calculate current streak of correct answers."""
        streak = 0
        for entry in reversed(history):
            if entry['correct']:
                streak += 1
            else:
                break
        return streak
    
    def _is_level_appropriate(self, recent_history: List[Dict]) -> bool:
        """Determine if current level is appropriate."""
        if len(recent_history) < self.minimum_questions:
            return True
            
        accuracy = sum(1 for x in recent_history if x['correct']) / len(recent_history)
        return self.accuracy_thresholds['downgrade'] <= accuracy <= self.accuracy_thresholds['upgrade']
    
    def should_adjust_difficulty(self, history: List[Dict]) -> Tuple[bool, str]:
        """Determine if difficulty should be adjusted."""
        if len(history) < self.minimum_questions:
            return False, "Need more questions"
            
        metrics = self.calculate_metrics(history)
        
        if metrics['accuracy'] >= self.accuracy_thresholds['upgrade']:
            return True, "upgrade"
        elif metrics['accuracy'] <= self.accuracy_thresholds['downgrade']:
            return True, "downgrade"
        
        return False, "maintain"

class ReportGenerator:
    """Generates performance reports and visualizations."""
    
    def generate_progress_chart(self, history: List[Dict]) -> Optional[px.line]:
        """Generate progress visualization."""
        if not history:
            return None
            
        df = pd.DataFrame(history)
        df['question_number'] = range(1, len(df) + 1)
        
        fig = px.line(
            df,
            x='question_number',
            y='accuracy',
            title='Learning Progress',
            labels={'question_number': 'Questions', 'accuracy': 'Accuracy'},
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Questions Attempted",
            yaxis_title="Accuracy",
            yaxis_range=[0, 1],
            showlegend=False
        )
        
        return fig
    
    def generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate personalized learning recommendations."""
        recommendations = []
        
        if metrics['total_questions'] < 3:
            recommendations.append("Complete more questions to get personalized recommendations.")
            return recommendations
            
        if metrics['accuracy'] < 0.4:
            recommendations.extend([
                "Review fundamental concepts before proceeding",
                "Focus on understanding basic principles",
                "Consider moving to an easier difficulty level"
            ])
        elif metrics['accuracy'] < 0.7:
            recommendations.extend([
                "You're making steady progress",
                "Pay attention to detailed explanations",
                "Practice similar questions to reinforce learning"
            ])
        else:
            recommendations.extend([
                "Excellent performance!",
                "Ready for more challenging questions",
                "Consider helping peers to reinforce your understanding"
            ])
        
        return recommendations

def format_time_taken(start_time: datetime) -> str:
    """Format the time taken for a question."""
    time_taken = datetime.now() - start_time
    minutes = time_taken.seconds // 60
    seconds = time_taken.seconds % 60
    return f"{minutes}m {seconds}s"