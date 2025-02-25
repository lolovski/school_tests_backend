import os
import subprocess
import time
import tempfile
import random
from http import HTTPStatus
from typing import List, Optional, Union

import psutil
from fastapi.params import Query
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.routers.utils import check_object_exists, check_name_duplicate, check_duplicate
from core.user_manager import current_user
from db.session import get_async_session
from app.schemes.problem import *
from requests.problem import *

router = APIRouter()

@router.get(
    '/problem/',
    response_model=List[ProblemRead],
    tags=['problem']
)
async def get_problems(
        session: AsyncSession = Depends(get_async_session),
        category_id: Optional[int] = Query(None),
        user: User = Depends(current_user)
):
    problems = await problem_requests.get_multi(category_id=category_id, session=session, user_id=user.id)
    return problems

@router.get(
    '/problem/{problem_id}',
    response_model=ProblemRead,
    tags=['problem']
)
async def get_problem(
        problem_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    problem = await problem_requests.get(id=problem_id, session=session)
    return problem

@router.post(
    '/problem/',
    response_model=ProblemRead,
    tags=['problem']
)
async def create_problem(
        problem_create: ProblemCreate,
        session: AsyncSession = Depends(get_async_session),
):
    problem = await problem_requests.create(obj_in=problem_create, session=session)
    return problem

@router.patch(
    '/problem/{problem_id}',
    response_model=ProblemRead,
    tags=['problem']
)
async def update_problem(
        problem_id: int,
        update_in: ProblemUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    problem = await check_object_exists(id=problem_id, requests=problem_requests, session=session)
    if update_in.name is not None:
        await check_name_duplicate(requests=problem_requests, session=session, name=update_in.name)
    problem = await problem_requests.update(problem, update_in, session=session)
    return problem

@router.delete(
    '/problem/{problem_id}',
    response_model=ProblemRead,
    tags=['problem']
)
async def delete_problem(
        problem_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    problem = await check_object_exists(id=problem_id, session=session, requests=problem_requests)
    problem = await problem_requests.remove(problem, session=session)
    return problem

@router.get(
    '/test/',
    response_model=List[TestRead],
    tags=['test']
)
async def get_tests(
        problem_id: Optional[int] = Query(None),
        session: AsyncSession = Depends(get_async_session),
):
    tests = await test_requests.get_multi(session=session, problem_id=problem_id)
    return tests

@router.get(
    '/test/{test_id}',
    response_model=TestRead,
    tags=['test']
)
async def get_test(
        test_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    test = await test_requests.get(id=test_id, session=session)
    return test

@router.post(
    '/test/',
    response_model=TestRead,
    tags=['test']
)
async def create_test(
        test_create: TestCreate,
        session: AsyncSession = Depends(get_async_session),
):
    test = await test_requests.create(test_create, session=session)
    return test

@router.patch(
    '/test/{test_id}',
    response_model=TestRead,
    tags=['test']
)
async def update_test(
        test_id: int,
        update_in: TestUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    test = await check_object_exists(id=test_id, requests=test_requests, session=session)
    test = await test_requests.update(test, update_in, session=session)

    return test

@router.delete(
    '/test/{test_id}',
    response_model=TestRead,
    tags=['test']
)
async def delete_test(
        test_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    test = await check_object_exists(id=test_id, requests=test_requests, session=session)
    test = await test_requests.remove(test, session=session)
    return test

@router.get(
    '/problem_category/',
    response_model=List[ProblemCategoryRead],
    tags=['problem category']
)
async def get_problem_categories(
        session: AsyncSession = Depends(get_async_session),
        parent_category_id: Optional[int] = Query(None)
):
    problem_categories = await problem_category_requests.get_multi(session=session, parent_category_id=parent_category_id)
    return problem_categories

@router.get(
    '/problem_category/{problem_category_id}',
    response_model=ProblemCategoryRead,
    tags=['problem category']
)
async def get_problem_category(
        problem_category_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    problem_category = await problem_category_requests.get(id=problem_category_id, session=session)
    return problem_category

@router.post(
    '/problem_category/',
    response_model=ProblemCategoryRead,
    tags=['problem category']
)
async def create_problem_category(
        problem_category_create: ProblemCategoryCreate,
        session: AsyncSession = Depends(get_async_session),
):
    problem_category = await problem_category_requests.create(problem_category_create, session=session)
    return problem_category

@router.patch(
    '/problem_category/{problem_category_id}',
    response_model=ProblemCategoryRead,
    tags=['problem category']
)
async def update_problem_category(
        problem_category_id: int,
        update_in: ProblemCategoryUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    problem_category = await check_object_exists(id=problem_category_id, requests=problem_category_requests, session=session)
    if update_in.name is not None:
        await check_name_duplicate(name=update_in.name, requests=problem_category_requests, session=session)
    problem_category = await problem_category_requests.update(problem_category, update_in, session=session)
    return problem_category

@router.delete(
    '/problem_category/{problem_category_id}',
    response_model=ProblemCategoryRead,
    tags=['problem category']
)
async def delete_problem_category(
        problem_category_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    problem_category = await check_object_exists(id=problem_category_id, requests=problem_category_requests, session=session)
    problem_category = await problem_category_requests.remove(problem_category, session=session)
    return problem_category

@router.get(
    '/user_problem/',
    tags=['user problem']
)
async def get_user_problem(
        user_id: Optional[int] = Query(None),
        problem_id: Optional[int] = Query(None),
        session: AsyncSession = Depends(get_async_session),
):
    user_problem = await user_problem_requests.get(user_id=user_id, problem_id=problem_id, session=session)
    return user_problem

@router.post(
    '/user_problem/',
    tags=['user problem']
)
async def create_user_problem(
        user_problem_create: UserProblemCreate,
        session: AsyncSession = Depends(get_async_session),
):
    async def create():
        problem_verdict = "OK"
        attempt = await user_problem_requests.get_count_attempts(user_id=user_id, problem_id=problem_id, session=session)
        attempt += 1
        for test_result in tests_results:
            await user_test_requests.create(
                UserTestCreate(
                    user_id=user_id,
                    problem_id=problem_id,
                    test_id=test_result['test_id'],
                    verdict=test_result['verdict'],
                    time=test_result['time'],
                    memory=test_result['memory'],
                    attempt=attempt,
                    user_output=test_result['user_output']
                ),
                session=session
            )
            if test_result['verdict'] != problem_verdict and problem_verdict == "OK":
                problem_verdict = test_result['verdict']

        db_user_problem = await user_problem_requests.create(
            UserProblemCreate(
                user_id=user_id,
                problem_id=problem_id,
                solution=code,
                verdict=problem_verdict,
                attempt=attempt
            ),
            session=session
        )

        return db_user_problem

    execution_time = memory_usage = 0
    code = user_problem_create.solution
    problem_id = user_problem_create.problem_id
    user_id = user_problem_create.user_id
    problem = await problem_requests.get(id=problem_id, session=session)
    # Запрашиваем тесты для этой карточки
    tests = await test_requests.get_multi(problem_id=problem_id, session=session)
    tests_results = []
    for test in tests:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode())
            temp_file_path = temp_file.name

        # Измеряем время выполнения и использование памяти
        start_time = time.time()
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss

        try:
            # Выполняем код и получаем вывод
            result = subprocess.run(["python", temp_file_path], input=test.input_data, text=True, capture_output=True,
                                    timeout=problem.time_limit)

            if result.stderr:
                os.remove(temp_file_path)
                tests_results.append({
                    'verdict': 'Ошибка компилятора',
                    'time': 0,
                    'memory': 0,
                    'test_id': test.id,
                    'user_output': 'Ответ отсутствует'
                })
                continue
            output = result.stdout.strip()
            execution_time = time.time() - start_time
            memory_after = process.memory_info().rss
            memory_usage = memory_after - memory_before

            if output != test.output_data:
                os.remove(temp_file_path)
                tests_results.append({
                    'verdict': 'Неверный ответ',
                    'time': execution_time,
                    'memory': memory_usage,
                    'test_id': test.id,
                    'user_output': output
                })
                continue

            if execution_time > problem.time_limit:  # Предположим, что 1 секунда - это лимит времени
                os.remove(temp_file_path)
                tests_results.append({
                    'verdict': 'Превышен лимит времени',
                    'time': execution_time,
                    'memory': memory_usage,
                    'test_id': test.id,
                    'user_output': 'Ответ отсутствует'
                })
                continue
            elif memory_usage > problem.memory_limit:  # Примерное значение для 100 МБ
                os.remove(temp_file_path)
                tests_results.append({
                    'verdict': 'Превышен лимит памяти',
                    'time': execution_time,
                    'memory': memory_usage,
                    'test_id': test.id,
                'user_output': 'Ответ отсутствует'
                })
                continue
            tests_results.append({
                'verdict': 'OK',
                'time': execution_time,
                'memory': memory_usage,
                'test_id': test.id,
                'user_output': output
            })
            os.remove(temp_file_path)

        except subprocess.TimeoutExpired:
            os.remove(temp_file_path)
            tests_results.append({
                'verdict': 'Превышен лимит времени',
                'time': execution_time,
                'memory': memory_usage,
                'test_id': test.id,
                'user_output': 'Ответ отсутствует'
            })
            continue

        except subprocess.CalledProcessError:
            os.remove(temp_file_path)
            tests_results.append({
                'verdict': 'Ошибка компилятора',
                'time': 0,
                'memory': 0,
                'test_id': test.id,
                'user_output': 'Ответ отсутствует'
            })
            continue

    db_obj = await create()

    return db_obj, tests_results

@router.delete(
    '/user_problem/',
    response_model=UserProblemRead,
    tags=['user problem']
)
async def delete_user_problem(
        user_id: int,
        problem_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    user_problem = await check_object_exists(user_id=user_id, problem_id=problem_id, session=session, requests=user_problem_requests)
    user_problem = await user_problem_requests.remove(user_problem, session=session)
    return user_problem