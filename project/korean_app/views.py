import math
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from konlpy.tag import Okt
from .models import Sentence, QuizResult, QuizLog
import random
from django.utils import timezone
from datetime import timedelta
# Okt 인스턴스를 전역 변수로 생성
okt = Okt()

pos_dict = {
    "Adjective": "형용사",
    "Adverb": "부사",
    "Alpha": "알파벳",
    "Conjunction": "접속사",
    "Determiner": "관형사",
    "Eomi": "어미",
    "Exclamation": "감탄사",
    "Foreign": "외국어",
    "Hashtag": "해시태그",
    "Josa": "조사",
    "KoreanParticle": "한국어 조사",
    "Noun": "명사",
    "Number": "숫자",
    "PreEomi": "선어말어미",
    "Punctuation": "구두점",
    "Suffix": "접미사",
    "Verb": "동사",
    "Modifier": "수식어",
}

pos_dict_description = {
    "형용사": "사물의 성질이나 상태를 나타내는 품사입니다. 예: 빠른, 아름다운",
    "부사": "주로 동사, 형용사, 다른 부사를 수식하는 품사입니다. 예: 매우, 빨리",
    "알파벳": "영어 알파벳을 나타냅니다. 예: a, b, c",
    "접속사": "단어, 구, 절, 문장 등을 이어주는 품사입니다. 예: 그리고, 하지만",
    "관형사": "체언 앞에서 체언을 꾸며주는 품사입니다. 예: 이, 그, 저",
    "어미": "용언의 어간에 붙어 문법적 기능을 수행하는 부분입니다. 예: -다, -고, -며",
    "감탄사": "감동이나 느낌을 나타내는 독립된 품사입니다. 예: 아!, 어머나!",
    "외국어": "한국어가 아닌 외국어 단어를 나타냅니다.",
    "해시태그": "소셜 미디어에서 사용되는 '#' 기호로 시작하는 태그입니다.",
    "조사": "체언 뒤에 붙어 그 말과 다른 말과의 관계를 나타내는 품사입니다. 예: 은, 는, 이, 가",
    "한국어 조사": "한국어 특유의 조사를 나타냅니다. 일반적인 조사와 구분됩니다.",
    "명사": "사물의 이름을 나타내는 품사입니다. 예: 책, 사람",
    "숫자": "수를 나타내는 단어입니다. 예: 1, 2, 3",
    "선어말어미": "어말 어미 앞에 오는 어미로, 시제나 상태 등을 나타냅니다. 예: -았-, -겠-",
    "구두점": "문장 부호를 나타냅니다. 예: ., ,, !, ?",
    "접미사": "단어의 뒤에 붙어 새로운 단어를 만드는 말입니다. 예: -적, -하다",
    "동사": "동작이나 작용을 나타내는 품사입니다. 예: 달리다, 먹다",
    "수식어": "명사나 형용사 앞에 붙어 그 명사나 형용사의 성질이나 상태를 나타내는 품사입니다. 예: 빨간, 큰",
}

def set_nickname(request):
    if request.method == "POST":
        nickname = request.POST.get("nickname", "Anonymous")
        request.session['nickname'] = nickname
        redirect_url = reverse('quiz')
        print(f"Redirecting to: {redirect_url}")  # 서버 콘솔에 로그 추가
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':          
            return JsonResponse({"status": "success", "redirect": redirect_url})
        else:
            return HttpResponseRedirect(redirect_url)
    return render(request, "korean_app/nickname.html")

def quiz(request):
    nickname = request.session.get('nickname')
    if not nickname:
        return redirect('set_nickname')
    
    # 새로운 QuizResult 객체 생성
    quiz_result = QuizResult.objects.create(
        nickname=nickname,
        score=0,
        time_taken=timedelta(seconds=0),
        completed_at=timezone.now()
    )
    request.session['quiz_result_id'] = quiz_result.id
    
    sentences = list(Sentence.objects.order_by('?')[:10])
    sentence = random.choice(sentences).text if sentences else "문장이 없습니다."

    # 전역 okt 인스턴스 사용
    morphemes_with_pos = okt.pos(sentence)
    morphemes_with_korean_pos = [(word, pos_dict.get(pos, pos)) for word, pos in morphemes_with_pos]
    
    if morphemes_with_korean_pos:
        quiz_item = random.choice(morphemes_with_korean_pos)
        quiz_word, quiz_pos = quiz_item
    else:
        quiz_word, quiz_pos = "", ""

    recent_results = QuizResult.objects.order_by('-completed_at')[:5]

    context = {
        "morphemes_with_pos": morphemes_with_korean_pos,
        "sentence": sentence,
        "quiz_word": quiz_word,
        "quiz_pos": quiz_pos,
        "recent_results": recent_results,
        "nickname": nickname,
        "pos_list": list(pos_dict.values()),  # 품사 목록 추가
        "pos_dict": pos_dict_description,
    }

    return render(request, "korean_app/korean_form.html", context)

def check_answer(request):
    if request.method == "POST":
        user_answer = request.POST.get("user_answer", "")
        correct_answer = request.POST.get("correct_answer", "")
        sentence = request.POST.get("sentence", "")
        target_word = request.POST.get("target_word", "")
        time_taken = int(request.POST.get("time_taken", 0))
        quiz_result_id = request.session.get('quiz_result_id')
        
        is_correct = user_answer.lower() == correct_answer.lower()
        
        if quiz_result_id:
            try:
                quiz_result = QuizResult.objects.get(id=quiz_result_id)
            except QuizResult.DoesNotExist:
                # quiz_result_id가 유효하지 않으면 새로운 QuizResult 객체 생성
                quiz_result = QuizResult.objects.create(
                    nickname=request.session.get('nickname', 'Anonymous'),
                    score=0,
                    time_taken=timedelta(seconds=0),
                    completed_at=timezone.now()
                )
                request.session['quiz_result_id'] = quiz_result.id
        else:
            # quiz_result_id가 없으면 새로운 QuizResult 객체 생성
            quiz_result = QuizResult.objects.create(
                nickname=request.session.get('nickname', 'Anonymous'),
                score=0,
                time_taken=timedelta(seconds=0),
                completed_at=timezone.now()
            )
            request.session['quiz_result_id'] = quiz_result.id

        QuizLog.objects.create(
            quiz_result=quiz_result,
            sentence=sentence,
            target_word=target_word,
            correct_answer=correct_answer,
            user_answer=user_answer,
            is_correct=is_correct,
            time_taken=timezone.timedelta(seconds=time_taken)
        )
        
        return JsonResponse({
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "user_answer": user_answer,
            "target_word": target_word
        })
    return JsonResponse({"error": "Invalid request method"})

def save_quiz_result(request):
    if request.method == "POST":
        score = int(request.POST.get("score", 0))
        time_taken = float(request.POST.get("time_taken", 0))
        nickname = request.session.get('nickname', 'Anonymous')
        quiz_result_id = request.session.get('quiz_result_id')
        
        time_taken_seconds = math.floor(time_taken)
        
        if quiz_result_id:
            try:
                quiz_result = QuizResult.objects.get(id=quiz_result_id)
                quiz_result.score = score
                quiz_result.time_taken = timedelta(seconds=time_taken_seconds)
                quiz_result.completed_at = timezone.now()
                quiz_result.save()
            except QuizResult.DoesNotExist:
                # quiz_result_id가 유효하지 않으면 새로운 QuizResult 객체 생성
                quiz_result = QuizResult.objects.create(
                    nickname=nickname,
                    score=score,
                    time_taken=timedelta(seconds=time_taken_seconds),
                    completed_at=timezone.now()
                )
        else:
            # quiz_result_id가 없으면 새로운 QuizResult 객체 생성
            quiz_result = QuizResult.objects.create(
                nickname=nickname,
                score=score,
                time_taken=timedelta(seconds=time_taken_seconds),
                completed_at=timezone.now()
            )
        
        # 세션에서 quiz_result_id 제거
        request.session.pop('quiz_result_id', None)
        
        return JsonResponse({
            "status": "success",
            "score": quiz_result.score,
            "time_taken": str(quiz_result.time_taken),
            "completed_at": quiz_result.completed_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({"status": "error", "message": "Invalid request method"})

def get_random_sentence(request):
    sentences = list(Sentence.objects.order_by('?')[:10])
    if sentences:
        selected_sentence = random.choice(sentences)
        morphemes = okt.pos(selected_sentence.text)
        selected_morpheme = random.choice(morphemes)
        return JsonResponse({
            'sentence': selected_sentence.text,
            'word': selected_morpheme[0],
            'pos': pos_dict.get(selected_morpheme[1], selected_morpheme[1])
        })
    return JsonResponse({'error': 'No sentences available'})

def show_results(request):
    results = QuizResult.objects.order_by('-completed_at')[:10]
    return render(request, "korean_app/results.html", {"results": results})