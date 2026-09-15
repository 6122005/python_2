"""Offline tests — cover everything that doesn't require a live API call.

Run with: pytest tests/ -v
"""
from __future__ import annotations

import json

import pytest

from src.memory.long_term import LongTermMemory
from src.memory.short_term import ShortTermMemory
from src.agents.react_agent import tool_search, tool_word_count


# --------------------------------------------------------------------------
# ShortTermMemory
# --------------------------------------------------------------------------


def test_short_term_records_turns_in_order():
    mem = ShortTermMemory(max_turns=5)
    mem.add_user("hello")
    mem.add_assistant("hi there")
    messages = mem.as_messages()
    assert messages == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi there"},
    ]


def test_short_term_evicts_oldest_turns_beyond_window():
    mem = ShortTermMemory(max_turns=2)  # keeps at most 4 messages
    for i in range(5):
        mem.add_user(f"question {i}")
        mem.add_assistant(f"answer {i}")
    messages = mem.as_messages()
    assert len(messages) == 4
    # oldest turns (question/answer 0, 1, 2) should be gone
    assert messages[0]["content"] == "question 3"


def test_short_term_rejects_invalid_max_turns():
    with pytest.raises(ValueError):
        ShortTermMemory(max_turns=0)


def test_short_term_clear():
    mem = ShortTermMemory()
    mem.add_user("hi")
    mem.clear()
    assert len(mem) == 0


# --------------------------------------------------------------------------
# LongTermMemory
# --------------------------------------------------------------------------


def test_long_term_persists_across_instances(tmp_path):
    path = tmp_path / "facts.json"
    mem1 = LongTermMemory(path)
    mem1.remember("favorite_language", "Python", session_id="s1")

    mem2 = LongTermMemory(path)  # simulates a fresh process / new session
    assert mem2.recall("favorite_language") == "Python"


def test_long_term_overwrites_existing_key(tmp_path):
    mem = LongTermMemory(tmp_path / "facts.json")
    mem.remember("favorite_language", "Python", session_id="s1")
    mem.remember("favorite_language", "JavaScript", session_id="s2")
    assert mem.recall("favorite_language") == "JavaScript"
    assert len(mem) == 1  # not a duplicate entry


def test_long_term_forget(tmp_path):
    mem = LongTermMemory(tmp_path / "facts.json")
    mem.remember("temp_fact", "value")
    mem.forget("temp_fact")
    assert mem.recall("temp_fact") is None


def test_long_term_handles_corrupt_file_without_crashing(tmp_path):
    path = tmp_path / "facts.json"
    path.write_text("{not valid json", encoding="utf-8")
    mem = LongTermMemory(path)  # should not raise
    assert mem.all_facts() == {}
    assert path.with_suffix(".corrupt.json").exists()


def test_as_system_context_empty_when_no_facts(tmp_path):
    mem = LongTermMemory(tmp_path / "facts.json")
    assert mem.as_system_context() == ""


def test_as_system_context_lists_known_facts(tmp_path):
    mem = LongTermMemory(tmp_path / "facts.json")
    mem.remember("user_name", "Jenish")
    context = mem.as_system_context()
    assert "user_name: Jenish" in context


# --------------------------------------------------------------------------
# ReAct agent tools (pure functions, no API call needed)
# --------------------------------------------------------------------------


def test_tool_search_hits_known_topic():
    result = tool_search("Tell me about LangGraph")
    assert "LangGraph" in result


def test_tool_search_misses_unknown_topic():
    result = tool_search("xyz123 nonsense topic")
    assert "No indexed results" in result


def test_tool_word_count():
    assert tool_word_count("one two three") == "3"


def test_tool_word_count_empty_string():
    assert tool_word_count("") == "0"


def test_tool_word_count_rejects_non_string_input():
    with pytest.raises(AttributeError):
        tool_word_count(12345)  # type: ignore[arg-type]
