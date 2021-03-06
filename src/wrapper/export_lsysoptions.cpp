/* ---------------------------------------------------------------------------
 #
 #       L-Py: L-systems in Python
 #
 #       Copyright 2003-2008 UMR Cirad/Inria/Inra Dap - Virtual Plant Team
 #
 #       File author(s): F. Boudon (frederic.boudon@cirad.fr)
 #
 # ---------------------------------------------------------------------------
 #
 #                      GNU General Public Licence
 #
 #       This program is free software; you can redistribute it and/or
 #       modify it under the terms of the GNU General Public License as
 #       published by the Free Software Foundation; either version 2 of
 #       the License, or (at your option) any later version.
 #
 #       This program is distributed in the hope that it will be useful,
 #       but WITHOUT ANY WARRANTY; without even the implied warranty of
 #       MERCHANTABILITY or FITNESS For A PARTICULAR PURPOSE. See the
 #       GNU General Public License for more details.
 #
 #       You should have received a copy of the GNU General Public
 #       License along with this program; see the file COPYING. If not,
 #       write to the Free Software Foundation, Inc., 59
 #       Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 #
 # ---------------------------------------------------------------------------
 */
#include <boost/python.hpp>

#include "lsysoptions.h"
using namespace boost::python;
LPY_USING_NAMESPACE

template <class T>
const typename T::element_type *get_item(T *obj, int index)
{
	size_t s = obj->size();
	if (index < 0)
		index += s;
	if (index < s)
		return *(obj->begin() + index);
	else
	{
		PyErr_SetString(PyExc_IndexError, "Out of range index.");
		boost::python::throw_error_already_set();
		return NULL;
	}
}

void export_Options()
{

	class_<LsysOptionValue, boost::noncopyable>
		// ("LsysOptionValue", init<const std::string&, optional<const std::string&> >
		// ("LsysOptionValue(name[,comment])",args("name","comment")))
		("LsysOptionValue", no_init)
			.enable_pickling()
			.def_readwrite("name", &LsysOptionValue::name)
			.def_readwrite("comment", &LsysOptionValue::comment)
			.def("activate", &LsysOptionValue::activate);
	class_<LsysOption, boost::noncopyable>("LsysOption", init<const std::string &, optional<const std::string &, const std::string &>>("LsysOption(name[,comment,category])", args("name", "comment", "category")))
		.enable_pickling()
		.def_readwrite("name", &LsysOption::name)
		.def_readwrite("comment", &LsysOption::comment)
		.def_readwrite("category", &LsysOption::category)
		.def_readwrite("default_value_id", &LsysOption::default_value_id)
		.def_readwrite("global", &LsysOption::global)
		.add_property("selection", &LsysOption::getCurrentValueId, &LsysOption::setCurrentValueId)
		.def("activate", &LsysOption::activate, args("value"))
		.def("activateSelection", &LsysOption::activateSelection)
		.def("setSelection", (bool (LsysOption::*)(const std::string &)) & LsysOption::setSelection)
		.def("setSelection", (bool (LsysOption::*)(size_t)) & LsysOption::setSelection)
		.def("__getitem__", &get_item<LsysOption>, return_internal_reference<>())
		.def("__len__", &LsysOption::size)
		.def("currentValue", &LsysOption::currentValue, return_value_policy<return_by_value>())
		.def("isToDefault", &LsysOption::isToDefault);
	class_<LsysOptions, boost::noncopyable>("LsysOptions", init<>("LsysOptions()"))
		.def("activate", &LsysOptions::activate, args("value"))
		.def("activateSelection", &LsysOptions::activateSelection)
		.def("setSelection", (bool (LsysOptions::*)(const std::string &, const std::string &)) & LsysOptions::setSelection)
		.def("setSelection", (bool (LsysOptions::*)(const std::string &, size_t)) & LsysOptions::setSelection)
		.def("find", &LsysOptions::find, return_internal_reference<>())
		.def("__getitem__", &get_item<LsysOptions>, return_internal_reference<>())
		.def("__len__", &LsysOptions::size);
}
