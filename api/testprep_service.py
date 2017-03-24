from data_helper import app, mongo
import pymongo

if __name__ != "__main__":
    db = mongo.db[app.config['MONGO_DBNAME']]


def query_user_skills_level(**kwargs):
    user_id = kwargs.get("user_id")
    program_id = kwargs.get("program_id")
    section_type = kwargs.get("section_type")
    level = kwargs.get("level")
    skill_type = kwargs.get("level")
    chapter_name = kwargs.get("chapter_name")

    result = []
    problem_query = {
        "program_id": int(program_id),
        "section_type": section_type,
        "level": int(level),
        "skill_type": skill_type,
        "chapter": chapter_name,
    }

    problem_cursor = db.test_prep_products_problems.find(problem_query, {'_id': False}) \
        .sort([("skill_seq", pymongo.ASCENDING)])
    if problem_cursor:
        for problem in problem_cursor:
            item = {}
            item["word"] = problem["section_id"]
            item["problem_type"] = problem["wordApplication_problemType"]
            item["level"] = get_user_skill_level(user_id=user_id,
                                                 program_id=program_id,
                                                 section_type=section_type,
                                                 level=level,
                                                 skill_type=skill_type,
                                                 keyword=item["word"])
            result.append(item)
    return result


def get_user_skill_level(**kwargs):
    user_id = kwargs.get("user_id")
    program_id = kwargs.get("program_id")
    section_type = kwargs.get("section_type")
    level = kwargs.get("level")
    skill_type = kwargs.get("level")
    keyword = kwargs.get("keyword")

    skill_status_query = {
        "user_id": user_id,
        "program_id": program_id,
        "section_type": section_type,
        "product_level": level,
        "skill_type": skill_type,
        "skill_section": keyword
    }

    skill = db.skill_status.find_one(skill_status_query)
    if skill:
        return skill["skill_status"]
    else:
        return 0


if __name__ == "__main__":
    from pymongo import MongoClient

    conn = MongoClient("mongodb://localhost//MathJoy")
    db = conn["MathJoy"]
    res = query_user_skills_level(user_id="",
                                  program_id="2",
                                  section_type="isee.vr",
                                  level=2,
                                  skill_type="Word Application",
                                  chapter_name="Chapter1")
    print res
